from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
from .models import UserProfile, Ticket
from django import forms
from .models import LeaveRequest

class SendTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = '__all__'

class TicketAdmin(admin.ModelAdmin):
    list_display = ('id_and_title','title', 'topic', 'created_by', 'created_at', 'assigned_to_display')
    list_filter = ('created_by', 'assigned_to')
    search_fields = ('title', 'topic', 'description')
    filter_horizontal = ('assigned_to',)

    def id_and_title(self, obj):
        return f"{obj.id} - {obj.title}"
    id_and_title.short_description = 'ID - Title'

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    def assigned_to_display(self, obj):
        return ', '.join([user.username for user in obj.assigned_to.all()])
    assigned_to_display.short_description = 'Assigned To'

admin.site.register(Ticket, TicketAdmin)




class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

class UserProfileAdminForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'

class UserProfileAdmin(admin.ModelAdmin):
    form = UserProfileAdminForm


from .models import LeaveRequest

class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'user_type')  # Отображаемые поля в списке



admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(LeaveRequest)