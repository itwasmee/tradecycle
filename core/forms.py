from django import forms


class ContactForm(forms.Form):
    email = forms.EmailField(
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'class': "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                }
            ))
    subject = forms.CharField(
        label='Sujet',
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'class': "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                }
            )
        )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': "shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                }
            )
        )

    def send_email(self):
        # send email using the self.cleaned_data dictionary
        pass
