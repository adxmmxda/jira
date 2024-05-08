from django.contrib.auth.models import User, Group
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

from django import forms    
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField('date published')


class Ticket(models.Model):
    STATUS_CHOICES = (
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('in_progress', 'In process'),
    )

    COMPONENT_CHOICES = (
        ('Tranzaxis Explorer', 'Tranzaxis Explorer'),
        ('Tranzaxis WEB-Explorer', 'Tranzaxis WEB-Explorer'),
        ('3DS Server', '3DS Server'),
        ('TXPG', 'TXPG'),
    )

    TYPE_CHOICES = (
        ('task', 'Задача'),
        ('question', 'Вопрос'),
    )

    title = models.CharField(max_length=200)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    component = models.CharField(max_length=50, choices=COMPONENT_CHOICES)
    topic = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tickets')
    sent_to = models.ManyToManyField(User, related_name='received_tickets', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    assigned_to = models.ManyToManyField(User, related_name='assigned_tickets', blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')  

    def __str__(self):
        return self.title
from django.shortcuts import render
from .models import Ticket






class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    ticket_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        if self.user:
            return f"Comment by {self.user.username} on {self.ticket.title}"
        else:
            return f"Comment on {self.ticket.title} (User not specified)"

class CommentFile(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    file = models.FileField(upload_to='comment_files/')

    def __str__(self):
        return self.file.name


class Project(models.Model):
    name = models.CharField(max_length=200)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    spitamen = models.BooleanField(default=False)
    sbt = models.BooleanField(default=False)
    matin = models.BooleanField(default=False)
    ssb = models.BooleanField(default=False)
    sarvat = models.BooleanField(default=False)
    vasl = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if self.spitamen:
            spitamen_group = Group.objects.get_or_create(name='Spitamen')[0]
            self.user.groups.add(spitamen_group)
        if self.sbt:
            sbt_group = Group.objects.get_or_create(name='Sbt')[0]
            self.user.groups.add(sbt_group)
        if self.matin:
            spitamen_group = Group.objects.get_or_create(name='Matin')[0]
            self.user.groups.add(spitamen_group)
        if self.ssb:
            sbt_group = Group.objects.get_or_create(name='Ssb')[0]
            self.user.groups.add(sbt_group)
        if self.sarvat:
            spitamen_group = Group.objects.get_or_create(name='Sarvat')[0]
            self.user.groups.add(spitamen_group)
        if self.vasl:
            sbt_group = Group.objects.get_or_create(name='Vasl')[0]
            self.user.groups.add(sbt_group)
        super().save(*args, **kwargs)

class CustomGroup(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    custom_field = models.CharField(max_length=100)

    def __str__(self):
        return self.group.name

from django.db import models

class LeaveRequest(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user_type = models.CharField(max_length=100)  

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.user_type}"





# from django.utils import timezone
# class TicketSubscription(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
#     subscribed_at = models.DateTimeField(default=timezone.now)

#     class Meta:
#         unique_together = ('user', 'ticket')

class Profiles(models.Model):
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)