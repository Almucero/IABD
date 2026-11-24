from django.contrib import admin

from .models import Article, SiteProfile


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "published_at", "is_published")
    list_filter = ("is_published",)
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "author")


@admin.register(SiteProfile)
class SiteProfileAdmin(admin.ModelAdmin):
    fields = ("site_name", "author_name", "biography")

    def has_add_permission(self, request):
        return not SiteProfile.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
