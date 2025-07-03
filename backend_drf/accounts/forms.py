from django import forms
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm

User = get_user_model()

class UserChangeForm(UserChangeForm):
  class Meta(UserChangeForm.Meta):
    model = User
    fields = ["first_name", 'last_name', 'email', 'password']

class UserCreationForm(admin_forms.UserCreationForm.Meta):
  class Meta(admin_forms.UserCreationForm.Meta):
    model = User
    fields = ["first_name", 'last_name', 'email', 'password']

  error_messages = {
    'duplicate_username': 'A user with that username alread exists',
    'duplicate_email': 'A user with that email alread exists'
  }

  def clean_email(self) -> str:
    email = self.cleaned_data['email']
    if User.objects.filter(email=email).exists():
      raise forms.ValidationError(self.error_messages['duplicated_email'])
    return email
    
  def clean_useraname(self) -> str:
    username = self.cleaned_data['username']
    if User.objects.filter(username=username).exists():
      raise forms.ValidationError(self.error_messages['duplicated_username'])
    return username
  


