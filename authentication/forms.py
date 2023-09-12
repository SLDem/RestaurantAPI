from django.contrib.auth.forms import UserCreationForm
from django import forms
from authentication.models import User


class SignupForm(UserCreationForm):
    email = forms.EmailField()
    name = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = (
            "email",
            "name",
        )
