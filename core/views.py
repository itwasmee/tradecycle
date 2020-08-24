from django.shortcuts import render
from django.views.generic.edit import FormView
from core.forms import ContactForm

# Create your views here.


class ContactPageView(FormView):
    form_class = ContactForm
    success_url = '/merci/'

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)
