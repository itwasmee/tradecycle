from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView
from django.views.generic.base import View
from django.views.generic.edit import CreateView

from .forms import AdPostForm
from .models import Ad, Favorite

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
    slug_field = "id"

    def post(self, *args, **kwargs):
        user = self.request.user
        ad_id = self.kwargs['pk']
        ad = Ad.objects.get(id=ad_id, user_id=user)
        ad.delete()
        return redirect('/')


class DetailAdView(DetailView):
    model = Ad
    pk_url_kwarg = "pk"


class FavoritesView(LoginRequiredMixin, ListView):
    model = Favorite
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(FavoritesView, self).get_context_data(**kwargs)
        user = self.request.user
        favs = Favorite.objects.filter(user=user)
        if favs.exists():
            context["favs"] = favs
        else:
            context["empty"] = True
        return context


class FavAddView(LoginRequiredMixin, View):
    model = Favorite
    slug_field = "id"

    def post(self, *args, **kwargs):
        user = self.request.user
        ad_id = self.kwargs['pk']
        ad = Ad.objects.get(id=ad_id)
        if Favorite.objects.filter(user=user, ad=ad).exists():
            Favorite.objects.filter(user=user, ad=ad).delete()
        else:
            fav = Favorite(user=user, ad=ad)
            fav.save()
        return redirect('/')
