from django.urls import path

from .views import (
    CategoryArticleListView,
    PublishedArticleDetailView,
    PublishedArticleListView,
)

urlpatterns = [
    path("", PublishedArticleListView.as_view(), name="home"),
    path(
        "categoria/<slug:slug>/",
        CategoryArticleListView.as_view(),
        name="category-detail",
    ),
    path(
        "articulo/<slug:slug>/",
        PublishedArticleDetailView.as_view(),
        name="article-detail",
    ),
]
