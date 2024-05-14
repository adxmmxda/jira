from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.views import PasswordResetConfirmView
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.exceptions import ValidationError
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse
from django.conf import settings
from .models import Ticket, Comment, Project
from .forms import TicketForm  
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from django.contrib.auth.models import Group
from .forms import CommentForm
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import EmailMultiAlternatives
from .models import Ticket, Comment, CommentFile  
from .forms import CommentForm, CommentFileForm
from django import forms
from .forms import AddUserForm 
import logging
from .models import LeaveRequest
from .models import Profiles
from .forms import ProfileForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Ticket
from .forms import TicketForm


logger = logging.getLogger(__name__)


def login_view(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            try:
                user_profile = UserProfile.objects.get(user=user)
                login(request, user)
                return redirect('user_tickets')

            except UserProfile.DoesNotExist:
                error_message = 'Пользователь не найден'
        else:
            error_message = password
            
        return render(request, 'login.html', {'error': error_message})
        
    
    return render(request, 'login.html')


def logout_view(request):
    pass


def home_view(request):
    return render(request, 'home.html')

def forgot_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            reset_view = PasswordResetView.as_view(template_name='password_reset.html')
            response = reset_view(request)
            if response.status_code == 302:
                uidb64 = response.context_data.get('uid')
                token = response.context_data.get('token')
                if (uidb64 and token):
                    return redirect(reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token}))
                else:
                    return render(request, 'password_reset_failed.html')  
        except User.DoesNotExist:
            error = 'Пользователь с таким именем не существует.'
            return render(request, 'login.html', {'error': error})

    return render(request, 'forgot_password.html')


def send_reset_email(user, uidb64, token):
    subject = 'Сброс пароля'
    from_email = 'nodir.akramzoda@yandex.ru'  # Замените на ваш адрес отправки
    to_email = user.email

    # Загрузите текстовый и HTML-шаблоны письма
    text_content = '...'
    html_content = render_to_string('password_reset_email.html', {'uidb64': uidb64, 'token': token})

    # Создайте письмо с обоими версиями (текстовой и HTML)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, "text/html")

    msg.send()

def password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        users = User.objects.filter(email=email)        
        if users.exists() and users.count() == 1:
            user = users.first()

            # Generate reset token and URL
            token = default_token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

            # Check if token is valid and generate reset URL
            current_site = "password_reset_confirm.html"#get_current_site(request)
            reset_url = reverse('password_reset_confirm', args=[uidb64, token])  # Изменен способ передачи параметров
            reset_url = f"http://{current_site}{reset_url}"

            send_reset_email(user, uidb64, token)

            messages.success(request, "На ваш адрес электронной почты отправлено письмо с инструкциями по сбросу пароля.")
            return redirect('password_reset')
        else:
            messages.error(request, "Пользователь с таким адресом электронной почты не найден.")
            return redirect('password_reset')

    return render(request, 'password_reset.html', {})

def password_reset_confirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = default_token_generator.check_token(uidb64, token)
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect('password_reset_complete')
            else:
                pass
        else:
            form = SetPasswordForm(user)
        return render(request, 'password_reset_confirm.html', {'form': form, 'uidb64': uidb64, 'token': token})
    else:
        return render(request, 'invalid_reset_link.html')

def invalid_reset_link(request):
    return render(request, 'invalid_reset_link.html')

def password_reset_complete(request):
    return render(request, 'password_reset_complete.html')
    
class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_reset.html' 

def password_reset_email(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            token = default_token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            
            subject = 'Сброс пароля'
            from_email = 'akramzodanodir5@gmail.com'  # Замените на ваш адрес отправки
            to_email = user.email

            # Загрузите текстовый и HTML-шаблоны письма
            text_content = '...'
            html_content = render_to_string('password_reset_email.html', {'uidb64': uidb64, 'token': token})

            # Создайте письмо с обоими версиями (текстовой и HTML)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
            msg.attach_alternative(html_content, "text/html")

            msg.send()

            return redirect('password_reset_complete')  # Перенаправление на страницу с подтверждением
    else:
        form = CustomPasswordResetForm()
    return render(request, 'forgot_password.html', {'form': form})

def my_view(request):

    user_profile = UserProfile.objects.get(user=request.user) 
    context = {'user_profile': user_profile}
    return render(request, 'tickets.html', context)

@login_required
def tickets(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = TicketForm(request.POST, request=request)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()
            # Добавьте тикет к текущему пользователю
            ticket.assigned_to.add(request.user)
            
            # После создания тикета, его статус должен быть установлен как "Открыт"
            ticket.status = 'open'
            ticket.save()
    
            return redirect('user_tickets')  # Редирект на страницу с тикетами пользователя
    else:
        form = TicketForm(request=request)
    return render(request, 'tickets.html', {
        'form': form,

        'spitamen': user_profile.spitamen,
        'sbt': user_profile.sbt,
        'matin': user_profile.matin,
        'ssb': user_profile.ssb,
        'sarvat': user_profile.sarvat,
        'vasl': user_profile.vasl
    })




from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import TicketForm

@login_required
def user_tickets(request):
    user_profile = UserProfile.objects.get(user=request.user)
    user = request.user
    users = User.objects.all()
    project_form = TicketForm()  # Создание формы для добавления проекта
    # tickets = Ticket.objects.filter(assigned_to=user)
    tickets = Ticket.objects.all()

    if request.method == 'POST':
        project_form = TicketForm(request.POST)
        if project_form.is_valid():
            ticket = project_form.save(commit=False)
            ticket.created_by = user
            ticket.status = 'open'
            ticket.save()
            ticket.assigned_to.add(user)
            tickets = Ticket.objects.filter(assigned_to=user)  # Обновляем список тикетов

    return render(request, 'user_tickets.html', {'tickets': tickets, 'users': users, 'project_form': project_form,
        'spitamen': user_profile.spitamen,
        'sbt': user_profile.sbt,
        'matin': user_profile.matin,
        'ssb': user_profile.ssb,
        'sarvat': user_profile.sarvat,
        'vasl': user_profile.vasl
    })
@login_required
def team_project(request):
    user_profile = UserProfile.objects.get(user=request.user)
    group_name = None
    
    # Определите группу пользователя
    if user_profile.spitamen:
        group_name = 'spitamen'
    elif user_profile.sbt:
        group_name = 'sbt'
    elif user_profile.matin:
        group_name = 'matin'
    elif user_profile.ssb:
        group_name = 'ssb'
    elif user_profile.sarvat:
        group_name = 'sarvat'
    elif user_profile.vasl:
        group_name = 'vasl'        
    # Другие группы
    
    # Фильтрация тикетов по группе пользователя
    if group_name:
        tickets = Ticket.objects.filter(group=group_name)
        group_tickets = True  # Переменная для указания, что отображаются только тикеты текущей группы
    else:
        tickets = Ticket.objects.all()  # Показать все тикеты, если группа не определена
        group_tickets = False  # Переменная для указания, что отображаются все тикеты
    
    return render(request, 'team_project.html', {'tickets': tickets, 'group_tickets': group_tickets,
        'spitamen': user_profile.spitamen,
        'sbt': user_profile.sbt,
        'matin': user_profile.matin,
        'ssb': user_profile.ssb,
        'sarvat': user_profile.sarvat,
        'vasl': user_profile.vasl
    })



# from .models import Ticket, TicketSubscription
# @login_required
# def tickets_all(request):
#     if request.method == 'POST':
#         ticket_id = request.POST.get('ticket_id')
#         ticket = Ticket.objects.get(id=ticket_id)
#         subscription, created = TicketSubscription.objects.get_or_create(user=request.user, ticket=ticket)
#         if created:
#             # Выводим сообщение о успешной подписке, если это первая подписка на этот тикет
#             # return render(request, 'subscription_success.html', {'ticket': ticket})
#             pass
#     tickets = Ticket.objects.all()
#     return render(request, 'tickets_all.html', {'tickets': tickets})




def projects(request):
    projects = Project.objects.all()
    return render(request, 'projects.html', {'projects': projects})

from django.shortcuts import redirect

from .models import Ticket, Comment, CommentFile  
from .forms import CommentForm, CommentFileForm  


from django.core.paginator import Paginator

from django.utils import timezone

@login_required
def add_comment(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    

    comments_per_page = 12
    comments = Comment.objects.filter(ticket=ticket).order_by('-created_at')


    paginator = Paginator(comments, comments_per_page)
    

    page_number = request.GET.get('page')
    

    comments_page = paginator.get_page(page_number)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        file_form = CommentFileForm(request.POST, request.FILES)

        if 'close_ticket' in request.POST:

            ticket.status = 'closed'
            ticket.save()

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.ticket = ticket
            comment.user = request.user
            comment.save()
            files = request.FILES.getlist('file')
            for f in files:
                comment_file = CommentFile(comment=comment, file=f)
                comment_file.save()


            if ticket.status == 'open':
                ticket.status = 'in_progress'
                ticket.save()


            redirect_url = reverse('add_comment', kwargs={'ticket_id': ticket_id}) + '?page=1'
            return redirect(redirect_url)
    else:
        comment_form = CommentForm()
        file_form = CommentFileForm()

    return render(request, 'add_comment.html', {'ticket': ticket, 'comments': comments_page, 'comment_form': comment_form, 'file_form': file_form})

from django.shortcuts import render

def leave_request(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        user_type = request.POST.get('user_type')

        LeaveRequest.objects.create(first_name=first_name, last_name=last_name, user_type=user_type)


        subject = 'Новая заявка на сайте'
        message = f'Получена новая заявка от {first_name} {last_name}.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [settings.ADMIN_EMAIL]  

        send_mail(subject, message, from_email, recipient_list)

        return redirect('login')

    return render(request, 'leave_request.html')


@login_required
def profile_modal(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_tickets')  
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'user_tickets.html', {'form': form, 'user': user})

from .forms import ProfileForm  

def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('profile')  
    else:
        form = ProfileForm()
    return render(request, 'profile.html', {'form': form})