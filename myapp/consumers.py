from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.urls import reverse
from .models import Ticket, Comment, CommentFile, UserProfile
from .forms import TicketForm, CommentForm, CommentFileForm
from django.contrib.auth.decorators import login_required

@login_required
def combined_view(request, ticket_id=None):
    user_profile = UserProfile.objects.get(user=request.user)
    user = request.user
    users = User.objects.all()
    project_form = TicketForm(request.POST or None, request=request)
    
    group_name = None
    groups = ['spitamen', 'sbt', 'matin', 'ssb', 'sarvat', 'vasl']
    for group in groups:
        if getattr(user_profile, group):
            group_name = group
            break
    
    tickets = Ticket.objects.filter(created_by=user)
    
    if request.method == 'POST' and not ticket_id:
        if project_form.is_valid():
            ticket = project_form.save(commit=False)
            ticket.created_by = user
            ticket.status = 'open'
            ticket.save()
            ticket.assigned_to.add(user)
            
            if ticket.group != group_name:
                ticket.save()
                tickets = Ticket.objects.filter(created_by=user)
    
    if ticket_id:
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
                
                redirect_url = reverse('user_tickets', kwargs={'ticket_id': ticket_id}) + '?page=1'
                return redirect(redirect_url)
        else:
            comment_form = CommentForm()
            file_form = CommentFileForm()
        
        return render(request, 'user_tickets.html', {
            'ticket': ticket,
            'comments': comments_page,
            'comment_form': comment_form,
            'file_form': file_form
        })
    
    return render(request, 'user_tickets.html', {
        'tickets': tickets,
        'users': users,
        'project_form': project_form,
        'spitamen': user_profile.spitamen,
        'sbt': user_profile.sbt,
        'matin': user_profile.matin,
        'ssb': user_profile.ssb,
        'sarvat': user_profile.sarvat,
        'vasl': user_profile.vasl
    })
