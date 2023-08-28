from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import CharField, TextInput, EmailField, EmailInput, PasswordInput


class RegisterForm(UserCreationForm):
    username = CharField(
        max_length=100, required=True, widget=TextInput(attrs={"class": "form-control"})
    )
    email = EmailField(
        max_length=150,
        required=True,
        widget=EmailInput(attrs={"class": "form-control"}),
    )
    password1 = CharField(
        max_length=50,
        min_length=8,
        required=True,
        widget=PasswordInput(attrs={"class": "form-control"}),
    )
    password2 = CharField(
        max_length=50,
        min_length=8,
        required=True,
        widget=PasswordInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ["username", "password"]
