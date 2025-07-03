from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from . forms import UserChangeForm, UserCreationForm

User = get_user_model()

@admin.register(User)
class UserAdmin(UserAdmin):
  form = UserChangeForm
  add_form = UserCreationForm
  list_display = ['pkid', 'id', 'email', 'username']
  search_fields = ['email', 'first_name', 'last_name']
  ordering = ['pkid']
  fieldsets = (
    (_('Loggin Credentials'),{'fields':('email', 'password')}),
    (_('Personal Info'),{'fields':('first_name', 'last_name', 'username')}),
    (_('Permission and Groups'),{'fields':('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    (_('Important Dates'),{'fields':('last_login', 'date_joined')}),  
  )
  add_fieldsets = ((None, {'classes': ('wide',),'fields':(
    'username',
    'email',
    'first_name',
    'last_name',
    'password1',
    'password2',

    )}),)
  


# Register your models here.
