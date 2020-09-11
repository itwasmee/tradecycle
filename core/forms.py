from django import forms
from core.models import Profile


class ContactForm(forms.Form):
    email = forms.EmailField(
        required=True,
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'class': "shadow appearance-none border rounded w-full py-2\
                px-3 text-gray-700 leading-tight focus:outline-none\
                focus:shadow-outline my-1"
                }
            )
        )
    subject = forms.CharField(
        required=True,
        label='Sujet',
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'class': "shadow appearance-none border rounded w-full py-2\
                px-3 text-gray-700 leading-tight focus:outline-none\
                focus:shadow-outline my-1"
                }
            )
        )
    message = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                'class': "shadow appearance-none border rounded w-full py-2\
                px-3 text-gray-700 leading-tight focus:outline-none\
                focus:shadow-outline my-1"
                }
            )
        )

    def send_email(self):
        # send email using the self.cleaned_data dictionary
        pass


class ProfileForm(forms.ModelForm):
    style = "appearance-none border rounded w-full py-2\
            px-3 leading-tight focus:outline-none\
            focus:shadow-outline my-2"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['picture'].widget.attrs['class'] = self.style
        self.fields['activity'].widget.attrs['class'] = self.style
        self.fields['activity'].initial = ''
        self.fields['activity'].widget.attrs['placeholder'] = 'example : Agriculteur'
        self.fields['location'].widget.attrs['class'] = self.style
        self.fields['location'].initial = ''
        self.fields['location'].widget.attrs['placeholder'] = 'example : Vire'

    class Meta:
        model = Profile
        fields = ('picture', 'activity', 'location')
        labels = {
            'picture': 'Image de profil',
            'activity': 'Votre activité',
            'location': 'Lieu de votre activité'
        }
