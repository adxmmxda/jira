from django.urls import path
from myapp.views import login_view, logout_view
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from myapp.views import home_view, forgot_password,password_reset, password_reset_confirm, invalid_reset_link, password_reset_complete, tickets, user_tickets, projects, add_comment, leave_request, profile_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', login_view),
    path('home/', home_view, name='home'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('password_reset/', password_reset, name='password_reset'),
    path('password_reset_confirm/<str:uidb64>/<str:token>/', password_reset_confirm, name='password_reset_confirm'),
    path('invalid_reset_link/', invalid_reset_link, name='invalid_reset_link'),
    path('password_reset_complete/', password_reset_complete, name='password_reset_complete'),
    path('tickets/', tickets, name='tickets'),
    path('user_tickets/', user_tickets, name='user_tickets'),
    path('projects/', projects, name='projects'),
    path('add_comment/<int:ticket_id>/', add_comment, name='add_comment'),
    path('leave_request/', leave_request, name='leave_request'),
    path('tickets/profile.html/', profile_view, name='profile_view'),
    path('user_tickets/profile.html/', profile_view, name='profile_view'),
    path('add_comment/profile.html/', profile_view, name='profile_view'),    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





