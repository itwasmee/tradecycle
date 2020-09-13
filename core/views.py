# from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from core.models import Profile
from core.forms import ContactForm, ProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.utils.datastructures import MultiValueDictKeyError
import os
from tradecycle.settings import MEDIA_ROOT


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
    slug_field = "user_id"

    def post(self, request, *args, **kwargs):
        user = get_user_model().objects.get(id=request.user.id)
        profile = Profile.objects.get(user=user.id)
        form = ProfileForm(request.POST)
        if form.is_valid():
            if request.FILES.get('picture'):
                profile.picture = request.FILES.get('picture')
                profile.picture.name = f"{user.id}.{profile.picture.name.lower().split('.').pop(1)}"
            if request.POST.get('activity') != '':
                profile.activity = request.POST.get('activity')
            if request.POST.get('location') != '':
                profile.location = request.POST.get('location')
            
            if Profile.objects.get(user=user).picture:
                name = "/user_profile/" + profile.picture.name
                location = MEDIA_ROOT
                path = location + name
                print(path)
                try:
                    os.remove(path)
                except FileNotFoundError:
                    print('NONE FOUND')
            profile.save()

        return redirect(f"/profil/{user.id}")
