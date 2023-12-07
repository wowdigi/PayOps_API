from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.auth import get_user_model

from .models import CustomUser


class CreateUserForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']


class ProfileModelForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = '__all__'
