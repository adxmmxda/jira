from django.urls import path, include
from . import views
from .views import home_view, forgot_password,password_reset, password_reset_confirm, invalid_reset_link, password_reset_complete, password_reset_failed, tickets, user_tickets, projects, add_comment, leave_request, profile_view, team_project





from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('home/', home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('password_reset_confirm/<str:uidb64>/<str:token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('password_reset_complete/', views.password_reset_complete, name='password_reset_complete'),
    path('invalid_reset_link/', views.invalid_reset_link, name='invalid_reset_link'),
    path('custom_password_reset/', views.CustomPasswordResetView.as_view(), name='custom_password_reset'),
    path('password_reset_failed/', password_reset_failed, name='password_reset_failed'),
    path('tickets/<int:ticket_id>/', views.tickets, name='tickets'),
    path('user_tickets/', views.user_tickets, name='user_tickets'),
    path('projects/', views.projects_view, name='projects'),
    path('add_comment/<int:ticket_id>/', views.add_comment, name='add_comment'),
    path('leave_request/', views.leave_request, name='leave_request'),
    path('tickets/profile.html', views.profile_view, name='profile_view'),
    path('user_tickets/profile.html', views.profile_view, name='profile_view'),
    path('add_comment/profile.html', views.profile_view, name='profile_view'),
    path('team_project/', views.team_project, name='team_project'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
