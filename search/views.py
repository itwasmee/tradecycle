from ad.models import Ad, Favorite
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.generic.list import ListView


class SearchView(ListView):
    """ displays ads related to the search terms or city"""
    model = Ad
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        query = self.request.GET.get("query")
        location = self.request.GET.get("location")

        if location is True and type(location) == str:
            queryset = Ad.objects.filter(
                title__unaccent__icontains=query  # unaccent is a Postgresql specific module
            ).filter(
                city__unaccent__icontains=location
            ).order_by('created_at')
        else:
            queryset = Ad.objects.filter(
                title__unaccent__icontains=query
            ).order_by('created_at')

        page = self.request.GET.get("page")
        paginator = Paginator(queryset, self.paginate_by)

        try:
            results = paginator.page(page)
        except PageNotAnInteger:
            results = paginator.page(1)
        except EmptyPage:
            results = paginator.page(paginator.num_pages)
        context["results"] = results
        context["query"] = query
        for ad in results:
            if self.request.user.id:
                ad.is_fav = Favorite.is_favorite(ad, self.request.user)
        return context
