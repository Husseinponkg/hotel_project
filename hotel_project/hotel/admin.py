from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile

# Registering the Profile model in the admin interface
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'culture_choice')  # Fields to display in the list view
    search_fields = ('user__username', 'culture_choice')  # Search functionality for the user and culture choice fields
    list_filter = ('culture_choice',)  # Filter by culture choice

# Register the Profile model to the admin interface
admin.site.register(Profile, ProfileAdmin)

# Optionally, you can also register the default User model to the admin if it's not already registered
admin.site.unregister(User)  # Unregister the default User model first
from django.contrib.auth.admin import UserAdmin

# Re-register the User model with custom configurations (if needed)
admin.site.register(User, UserAdmin)
