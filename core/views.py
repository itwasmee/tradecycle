import os

from ad.models import Ad
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from tradecycle.settings import DEFAULT_FROM_EMAIL, MEDIA_ROOT
from PIL import Image

from core.forms import ContactForm, MessageForm, ProfileForm
from core.models import Profile


class ContactPageView(FormView):
    """ view that displays the contact form"""

    form_class = ContactForm
    success_url = "/thank-you/"

    def form_valid(self, form):
        """if the form is valid, sends the email with following args"""
        send_mail(
            subject=form.cleaned_data.get("subject"),
            message=form.cleaned_data.get("message"),
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[form.cleaned_data.get("email")],
        )
        return super(ContactPageView, self).form_valid(form)


class ProfilePageView(LoginRequiredMixin, DetailView, FormView):
    """ this view displays the user details, allows for profile changes and displays his posted ads"""

    model = Profile
    form_class = ProfileForm

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def form_valid(self, form):
        user = get_user_model().objects.get(id=self.request.user.id)
        profile = Profile.objects.get(user=user.id)
        if form.instance.picture:  # renaming of the image
            profile.picture = form.instance.picture
            profile.picture.name = (
                f"{user.id}.{profile.picture.name.lower().split('.').pop(1)}"
            )

        if form.instance.activity != "":
            profile.activity = form.instance.activity
        if form.instance.location != "":
            profile.location = form.instance.location
        if Profile.objects.get(
            user=user
        ).picture:  # remove old picture if new one is submitted
            name = "/user_profile/" + profile.picture.name
            location = MEDIA_ROOT
            path = location + name
            try:
                os.remove(path)
            except FileNotFoundError:
                print(f"No picture found at {path}")
        profile.save()
        lower_quality(
            MEDIA_ROOT + profile.picture.url
        )  # lower resolution for profile picture
        return redirect("/profil/")

    def get_context_data(self, **kwargs):
        """ context : ads posted by user"""
        context_data = super(ProfilePageView, self).get_context_data(**kwargs)
        user = get_user_model().objects.get(username=self.request.user)
        user_ads = Ad.objects.filter(user_id=user)
        context_data["user_ads"] = user_ads
        return context_data


def lower_quality(path):
    """lowers the qulity of the image posted

    Args:
        path (str): path of the submitted img
    """
    image_file = Image.open(path)
    image_file.save(path, quality=50)


class SendMessageView(FormView, DetailView):
    """ Displays form used to send a message to the poster of the ad and sends it upon form validation"""

    model = Ad
    form_class = MessageForm

    def form_valid(self, form, **kwargs):
        """ the email is sent if the form is valid"""
        ad_id = self.kwargs["pk"]
        ad = Ad.objects.get(id=ad_id)
        user = get_user_model().objects.get(username=ad.user_id)
        send_mail(
            f"{form.cleaned_data.get('name')} via Tradecycle",
            form.cleaned_data.get("message"),
            from_email="tradecycler@gmail.com",
            recipient_list=[user.email],
        )
        return redirect("/")


class FavoritesView(LoginRequiredMixin, ListView):
    model = Ad
    paginate_by = 20
    
    def get_context_data(self, request):
        pass