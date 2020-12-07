from django.shortcuts import render
from django.views.generic.list import ListView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from ad.models import Ad


class SearchView(ListView):
    """ displays ads related to the search terms or city"""
    model = Ad
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        query = self.request.GET.get("query")
        location = self.request.GET.get("location")

        if location is True:
            queryset = Ad.objects.filter(
                title__unaccent__icontains=query  # unaccent is a Postgresql specific module
            ).filter(
                city__unaccent__icontains=location
            ).order_by('created_at')
        else:
            queryset = Ad.objects.filter(
                title__unaccent__icontains=query  # TODO add 'field required' to one field only
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
        return context
