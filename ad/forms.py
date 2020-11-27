from django import forms
from .models import Ad


class AdPostForm(forms.ModelForm):
    style = "appearance-none border rounded w-full py-2\
            px-3 leading-tight focus:outline-none\
            focus:shadow-outline my-2"

    style_radio = "justify-around  flex w-full py-2\
            px-3 leading-tight focus:outline-none\
            my-1"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = self.style
        self.fields['title'].widget.attrs['required'] = "required"
        self.fields['description'].widget.attrs['class'] = self.style
        self.fields['description'].widget.attrs['required'] = "required"
        self.fields['action'].widget.attrs['class'] = self.style_radio
        self.fields['action'].widget.attrs['required'] = "required"
        self.fields['image'].widget.attrs['class'] = self.style
        '''self.fields['image'].widget.attrs['required'] = "required"'''
        self.fields['city'].widget.attrs['class'] = self.style
        self.fields['city'].widget.attrs['required'] = "required"

    class Meta:
        model = Ad
        fields = ["action", "title", "description", "city", "image"]
        labels = {
            "title": "Titre",
            "action": "Vous",
            "description": "Description",
            "image": "Ajoutez une image",
            "city": "Lieu"
        }
        widgets = {
            "action": forms.RadioSelect()
        }
