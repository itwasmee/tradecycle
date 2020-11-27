# from django.shortcuts import render
import os

from ad.models import Ad
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from tradecycle.settings import MEDIA_ROOT

from core.forms import ContactForm, ProfileForm
from core.models import Profile

# Create your views here.


class ContactPageView(FormView):
    form_class = ContactForm
    success_url = '/merci/'

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)


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
