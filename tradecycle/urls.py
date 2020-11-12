"""tradecycle URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth.views import LoginView, LogoutView
from accounts.forms import UserRegistrationForm, AuthenticationForm
from django.views.generic.base import TemplateView
from django.views.generic import CreateView
from core.views import ContactPageView, ProfilePageView
from search.views import SearchView
from ad.views import AdPostView, DeleteAdView, DetailView

urlpatterns = [
    path(
        'admin/',
        admin.site.urls
    ),
    path(
        '',
        TemplateView.as_view(template_name='accueil.html'),
        name='accueil'
    ),
    path(
        'a-propos/',
        TemplateView.as_view(template_name='a-propos.html'),
        name='a-propos'
    ),
    path(
        'contact/',
        ContactPageView.as_view(template_name='contact.html'),
        name='contact'
    ),
    path(
        'profil/<slug>',
        ProfilePageView.as_view(template_name='profil.html'),
        name='profil'
    ),
    path(
        "login/",
        LoginView.as_view(
            template_name="login.html",
            form_class=AuthenticationForm,
            success_url="/",
            ),
        name="login"
    ),
    path(
        "logout/",
        LogoutView.as_view(
            template_name="logout.html"
        ),
        name="logout",
    ),
    path(
        "signup/",
        CreateView.as_view(
            template_name="signup.html",
            form_class=UserRegistrationForm,
            success_url='/login'
        ),
        name="signup",
    ),
    path(
        "recherche/",
        SearchView.as_view(),
        name="recherche",
    ),
    path(
        "deposer-une-annonce/",
        AdPostView.as_view(
            template_name='deposer-une-annonce.html'
        ),
        name="deposer-une-annonce",
    ),
    path(
        "delete_ad/<pk>",
        DeleteAdView.as_view(),
        name="supprimer",
    ),
    path(
        "search/",
        SearchView.as_view(template_name="search.html"),
        name="search",
    ),
    path(
        "ad/<pk>",
        DetailView.as_view(
            template_name="ad.html"
        ),
        name="ad",
    ),
    path('', include('django_private_chat.urls'))
]
