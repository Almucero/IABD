from django.views.generic import DetailView, ListView
from django.shortcuts import get_object_or_404

from .models import Article, Category


class PublishedArticleListView(ListView):
    model = Article
    template_name = "articles/article_list.html"
    context_object_name = "articles"

    def get_queryset(self):
        return Article.objects.filter(is_published=True).select_related("category")


class CategoryArticleListView(PublishedArticleListView):
    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs["slug"])
        return super().get_queryset().filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        return context


class PublishedArticleDetailView(DetailView):
    model = Article
    template_name = "articles/article_detail.html"
    context_object_name = "article"

    def get_queryset(self):
        return Article.objects.filter(is_published=True).select_related("category")
