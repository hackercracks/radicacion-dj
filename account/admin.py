from django.contrib import admin
from .models import UserProfile, User, FailedLogin


@admin.register(UserProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']


admin.site.register(User)
admin.site.register(FailedLogin)