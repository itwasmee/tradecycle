# from django.shortcuts import render
import os

from ad.models import Ad
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from tradecycle.settings import MEDIA_ROOT, DEFAULT_FROM_EMAIL
from django.core.mail import send_mail
from core.forms import ContactForm, ProfileForm, MessageForm
from core.models import Profile

# Create your views here.


class ContactPageView(FormView):
    
    form_class = ContactForm
    success_url = '/contact/'

    def form_valid(self, form):
        send_mail(subject=form.cleaned_data.get('subject'), message=form.cleaned_data.get('message'), from_email=DEFAULT_FROM_EMAIL, recipient_list=[form.cleaned_data.get('email')])
        return super(ContactPageView, self).form_valid(form)


class ProfilePageView(LoginRequiredMixin, DetailView, FormView):
    model = Profile
    form_class = ProfileForm

    def get_object(self):
        return Profile.objects.get(user=self.request.user)
    
    def form_valid(self, form):
        user = get_user_model().objects.get(id=self.request.user.id)
        profile = Profile.objects.get(user=user.id)
        if form.instance.picture:
            profile.picture = form.instance.picture
            profile.picture.name = (
                f"{user.id}.{profile.picture.name.lower().split('.').pop(1)}"
            )
        if form.instance.activity != '':
            profile.activity = form.instance.activity
        if form.instance.location != '':
            profile.location = form.instance.location
        if Profile.objects.get(user=user).picture:
            name = "/user_profile/" + profile.picture.name
            location = MEDIA_ROOT
            path = location + name
            try:
                os.remove(path)
            except FileNotFoundError:
                print(f'No picture found at {path}')
        profile.save()
        # TODO:Image crop
        return redirect("/profil/")

    def get_context_data(self, **kwargs):
        context_data = super(ProfilePageView, self).get_context_data(**kwargs)
        user = get_user_model().objects.get(username=self.request.user)
        user_ads = Ad.objects.filter(user_id=user)
        context_data["user_ads"] = user_ads
        return context_data


class SendMessageView(LoginRequiredMixin, FormView, DetailView):
    model = Ad
    form_class = MessageForm

    def form_valid(self, form, **kwargs):
        ad_id = self.kwargs['pk']
        ad = Ad.objects.get(id=ad_id)
        username = self.request.user.username
        user = get_user_model().objects.get(username=ad.user_id)
        send_mail(f"{username} via Tradecycle", form.cleaned_data.get('message'), from_email="tradecycler@gmail.com", recipient_list=[user.email])
        return redirect("/")
