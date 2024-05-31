from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Ticket
from django.contrib.auth.forms import UserCreationForm
from .models import Comment
from .models import CommentFile
from django.contrib.auth.models import Group
from .models import Ticket, UserProfile
from django.contrib.auth.models import User
from .models import Profiles




'''class LoginForm(AuthenticationForm):
    pass'''

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'component', 'type', 'topic', 'description', 'assigned_to', 'group']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(TicketForm, self).__init__(*args, **kwargs)
        self.fields['topic'].widget.attrs.update({'class': 'your-class-name'})
        self.fields['description'].widget.attrs.update({'placeholder': 'Type a description:'})  # Добавление placeholder'а для поля описания

        # Фильтрация групп на основе пользователя
        user_profile = UserProfile.objects.get(user=self.request.user)
        
        if user_profile.spitamen:
            group_choices = [
                ('spitamen', 'Spitamen'),
                ('sbt', 'Sbt'),
                ('matin', 'Matin'),
                ('ssb', 'Ssb'),
                ('sarvat', 'Sarvat'),
                ('vasl', 'Vasl')
            ]
        else:
            group_choices = [('spitamen', 'Public')]
            if user_profile.sbt:
                group_choices.append(('sbt', 'Private'))
            if user_profile.matin:
                group_choices.append(('matin', 'Private'))
            if user_profile.ssb:
                group_choices.append(('ssb', 'Private'))
            if user_profile.sarvat:
                group_choices.append(('sarvat', 'Private'))
            if user_profile.vasl:
                group_choices.append(('vasl', 'Private'))
        
        self.fields['group'].choices = group_choices

    def save(self, commit=True):
        ticket = super().save(commit=False)
        if commit:
            ticket.created_by = self.request.user
            ticket.save() 
        return ticket


class AddUserForm(forms.Form):
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'Введите ваш комментарий здесь'}),
        }


class CommentFileForm(forms.ModelForm):
    class Meta:
        model = CommentFile
        fields = ['file']



class SendTicketForm(forms.Form):
    sent_to = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )  

from .models import LeaveRequest

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profiles
        fields = ['profile_picture']  # Укажите только поле аватара

