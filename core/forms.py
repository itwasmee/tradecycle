from django import forms
from core.models import Profile


class ContactForm(forms.Form):
    """Contact form for visiters, used for feedback and suggestions"""
    email = forms.EmailField(
        required=True,
        max_length=200,
        widget=forms.TextInput(
            attrs={
                "class": "shadow appearance-none border rounded w-full py-2\
                px-3 text-gray-700 leading-tight focus:outline-none\
                focus:shadow-outline my-1"
            }
        ),
    )
    subject = forms.CharField(
        required=True,
        label="Sujet",
        max_length=200,
        widget=forms.TextInput(
            attrs={
                "class": "shadow appearance-none border rounded w-full py-2\
                px-3 text-gray-700 leading-tight focus:outline-none\
                focus:shadow-outline my-1"
            }
        ),
    )
    message = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                "class": "shadow appearance-none border rounded w-full py-2\
                px-3 text-gray-700 leading-tight focus:outline-none\
                focus:shadow-outline my-1"
            }
        ),
    )


class ProfileForm(forms.ModelForm):
    """this form allows the user to change his profile picture, activity and location"""

    style = "appearance-none border rounded w-full py-2\
            px-3 leading-tight focus:outline-none\
            focus:shadow-outline my-2"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["picture"].widget.attrs["class"] = self.style
        self.fields["activity"].widget.attrs["class"] = self.style
        self.fields["activity"].initial = ""
        self.fields["activity"].widget.attrs["placeholder"] = "example : Agriculteur"
        self.fields["location"].widget.attrs["class"] = self.style
        self.fields["location"].initial = ""
        self.fields["location"].widget.attrs["placeholder"] = "example : Normandie"

    class Meta:
        model = Profile
        fields = ("picture", "activity", "location")
        labels = {
            "picture": "Image de profil",
            "activity": "Votre activité",
            "location": "Lieu de votre activité",
        }


class MessageForm(forms.Form):
    name = forms.CharField(
        required=True,
        label="Nom",
        max_length=200,
        widget=forms.TextInput(
            attrs={
                "class": "shadow appearance-none border rounded w-full py-2\
                px-3 text-gray-700 leading-tight focus:outline-none\
                focus:shadow-outline my-1"
            }
        ),
    )
    email = forms.EmailField(
        required=True,
        max_length=200,
        widget=forms.TextInput(
            attrs={
                "class": "shadow appearance-none border rounded w-full py-2\
                px-3 text-gray-700 leading-tight focus:outline-none\
                focus:shadow-outline my-1"
            }
        ),
    )
    message = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                "class": "shadow appearance-none border rounded w-full py-2\
                px-3 text-gray-700 leading-tight focus:outline-none\
                focus:shadow-outline my-1"
            }
        ),
    )
