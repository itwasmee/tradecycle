import os

from ad.models import Ad
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from tradecycle.settings import DEFAULT_FROM_EMAIL, MEDIA_ROOT

from core.forms import ContactForm, MessageForm, ProfileForm
from core.models import Profile


class ContactPageView(FormView):
    """ view that displays the contact form"""

    form_class = ContactForm
    success_url = "/merci/"

    def form_valid(self, form):
        """if the form is valid, sends the email with following args"""
        send_mail(
            subject=form.cleaned_data.get("subject"),
            message=form.cleaned_data.get("message"),
            from_email=form.cleaned_data.get("email"),
            recipient_list=[DEFAULT_FROM_EMAIL],
        )
        return super(ContactPageView, self).form_valid(form)


class ProfilePageView(LoginRequiredMixin, DetailView, FormView):
    """ this view displays the user details, allows for profile changes and displays his posted ads"""

    model = Profile
    form_class = ProfileForm
    paginate_by = 10

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def form_valid(self, form):
        user = get_user_model().objects.get(id=self.request.user.id)
        profile = Profile.objects.get(user=user.id)
        print(form.instance.picture)
        if form.instance.picture == "profile/user.svg": # default image set in models
            pass
        elif form.instance.picture:  
            if Profile.objects.get(user=user).picture:  
                print(Profile.objects.get(user=user).picture.name)
                name = profile.picture.name
                location = MEDIA_ROOT
                path = location + name
            try: # remove old picture if new one is submitted
                os.remove(path)
                print(path, 'deleted')
            except FileNotFoundError:
                print(f"No picture found at {path}")

            profile.picture = form.instance.picture
            profile.picture.name = (
                f"{user.username}.{profile.picture.name.lower().split('.').pop(1)}" # renaming of the image
            )
        else:
            pass
        if form.instance.activity != "":
            profile.activity = form.instance.activity
        if form.instance.location != "":
            profile.location = form.instance.location
        
        profile.save()
        return redirect("/profil/")

    def get_context_data(self, **kwargs):
        """ context : ads posted by user"""
        context_data = super(ProfilePageView, self).get_context_data(**kwargs)
        user = get_user_model().objects.get(username=self.request.user)
        ads = Ad.objects.filter(user_id=user).order_by("created_at")
        page = self.request.GET.get("page")
        paginator = Paginator(ads, self.paginate_by)

        try:
            ads = paginator.page(page)
        except PageNotAnInteger:
            ads = paginator.page(1)
        except EmptyPage:
            ads = paginator.page(paginator.num_pages)
        context_data["user_ads"] = ads
        return context_data


class SendMessageView(FormView, DetailView):
    """ Displays form used to send a message to the poster of the ad and sends
    it upon form validation"""

    model = Ad
    form_class = MessageForm
    success_url = "/message-envoye/"

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
        return HttpResponse()
