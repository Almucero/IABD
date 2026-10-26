from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView

from .models import Article, SiteProfile


class PublishedArticleListView(ListView):
    model = Article
    template_name = "articles/article_list.html"
    context_object_name = "articles"

    def get_queryset(self):
        return Article.objects.filter(is_published=True)


class PublishedArticleDetailView(DetailView):
    model = Article
    template_name = "articles/article_detail.html"
    context_object_name = "article"

    def get_queryset(self):
        return Article.objects.filter(is_published=True)


def about(request):
    profile = get_object_or_404(SiteProfile, pk=1)
    return render(request, "articles/about.html", {"profile": profile})
