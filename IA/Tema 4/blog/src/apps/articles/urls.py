from django.urls import path

from .views import PublishedArticleDetailView, PublishedArticleListView, about

urlpatterns = [
    path("", PublishedArticleListView.as_view(), name="home"),
    path(
        "articulos/<slug:slug>/",
        PublishedArticleDetailView.as_view(),
        name="article-detail",
    ),
    path("sobre-mi/", about, name="about"),
]
