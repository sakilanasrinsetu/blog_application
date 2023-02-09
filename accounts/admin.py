from django.contrib import admin
from accounts.models import UserAccount

# Register your models here.

class UserAccountAdmin(admin.ModelAdmin):
    list_display = ['id','username','first_name', 'last_name', 'email', 'is_employee']

    class Meta:
        model = UserAccount

admin.site.register(UserAccount, UserAccountAdmin)