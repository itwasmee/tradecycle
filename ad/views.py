from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import DetailView
from django.views.generic.base import View
from django.views.generic.edit import CreateView

from .forms import AdPostForm
from .models import Ad

# Create your views here.


class AdPostView(LoginRequiredMixin, CreateView):
    form_class = AdPostForm
    model = Ad
    success_url = '/'

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        form.instance.image.name = f"ad_{form.instance.user_id}.jpg"
        return super().form_valid(form)


class DeleteAdView(LoginRequiredMixin, View):
    model = Ad
    success_url = "/"
    slug_field = "id"

    def get(self, *args, **kwargs):
        user = self.request.user
        ad_id = self.kwargs['pk']
        ad = Ad.objects.get(id=ad_id, user_id=user)
        ad.delete()
        return redirect('/')


class DetailAdView(DetailView):
    model = Ad
    pk_url_kwarg = "pk"
