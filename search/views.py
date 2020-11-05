from django.shortcuts import render
from django.views.generic.list import ListView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from ad.models import Ad


# Create your views here.


class SearchView(ListView):
    model = Ad
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        query = self.request.GET.get("query")
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
        return context
