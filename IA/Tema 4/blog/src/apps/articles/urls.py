from django.urls import path

from .api_views import (
    PublishedArticleDetailAPIView,
    PublishedArticleListCreateAPIView,
)
from .views import PublishedArticleDetailView, PublishedArticleListView, about

urlpatterns = [
    path("", PublishedArticleListView.as_view(), name="home"),
    path(
        "api/articulos/",
        PublishedArticleListCreateAPIView.as_view(),
        name="api-article-list",
    ),
    path(
        "api/articulos/<int:pk>/",
        PublishedArticleDetailAPIView.as_view(),
        name="api-article-detail",
    ),
    path(
        "articulos/<slug:slug>/",
        PublishedArticleDetailView.as_view(),
        name="article-detail",
    ),
    path("sobre-mi/", about, name="about"),
]
