from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (AuthenticationForm, UserChangeForm,
                                       UserCreationForm)
from django.utils.translation import gettext_lazy as _


class UserRegistrationForm(UserCreationForm):
    style = "appearance-none border rounded w-full py-2\
            px-3 leading-tight focus:outline-none\
            focus:shadow-outline my-2"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs["class"] = self.style
        self.fields["username"].widget.attrs["class"] = self.style
        self.fields["username"].help_text = None

    error_messages = {
        "password_mismatch": _("Les mots de passes no correspondent pas."),
    }

    password1 = forms.CharField(
        label=_("Mot de passe"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": style}
        ),
    )
    password2 = forms.CharField(
        label=_("Confirmation mot de passe"),
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": style}
        ),
        strip=False,
    )

    class Meta:
        model = get_user_model()
        fields = ("email", "username")
        labels = {
            "email": "Email",
            "username": "Nom utilisateur ou Nom de l'entreprise",
        }


class AuthenticationForm(AuthenticationForm):
    style = "appearance-none border rounded w-full py-2\
            px-3 leading-tight focus:outline-none\
            focus:shadow-outline my-2"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].widget.attrs["class"] = self.style
        self.fields["password"].label = "Mot de passe"

    username = forms.CharField(
        required=True,
        max_length=200,
        widget=forms.TextInput(attrs={"class": style, "autocomplete": "email"}),
        label="Email ou Nom d'utilisateur",
    )

    class Meta:
        model = get_user_model()
        fields = ["email", "password"]


# for admin panel
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "email")


# for admin panel
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "email")
