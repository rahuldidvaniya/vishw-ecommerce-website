from django.contrib import admin
from userauths.models import User, Profile, Address

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']

    def has_change_permission(self, request, obj=None):
        return False


from django.core.exceptions import PermissionDenied



class ProfileAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone']
    readonly_fields = ['user', 'username', 'first_name', 'last_name', 'image', 'phone', 'secondary_phone', 'email']  # Specify fields you want to make read-only

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def add_view(self, request, form_url='', extra_context=None):
        raise PermissionDenied("Adding profiles manually is not allowed.")

    





class AddressAdmin(admin.ModelAdmin):
    list_display = ['user']

    def has_change_permission(self, request, obj=None):
        return False

admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Address, AddressAdmin)
