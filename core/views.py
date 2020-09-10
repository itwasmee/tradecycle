# from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from core.models import Profile
from core.forms import ContactForm, ProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

# Create your views here.


class ContactPageView(FormView):
    form_class = ContactForm
    success_url = '/merci/'

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)


class ProfilePageView(LoginRequiredMixin, DetailView, FormView):
    model = get_user_model()
    form_class = ProfileForm

    def get_object(self):
        return self.request.user
