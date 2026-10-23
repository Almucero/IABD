from django.contrib import admin

from .models import Article, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "is_published", "published_at")
    list_filter = ("is_published", "category")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title",)
