from django.db import models
from django.utils import timezone


class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    summary = models.CharField(max_length=300)
    body = models.TextField()
    author = models.CharField(max_length=150, default="Autor/a del blog")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)
    is_published = models.BooleanField(
        "Publicado",
        default=False,
        help_text="Activa esta casilla para mostrar el artículo en el blog.",
    )

    class Meta:
        verbose_name = "artículo"
        verbose_name_plural = "artículos"
        ordering = ("-published_at", "-created_at")

    def save(self, *args, **kwargs):
        if self.is_published and self.published_at is None:
            self.published_at = timezone.now()
            update_fields = kwargs.get("update_fields")
            if update_fields is not None:
                kwargs["update_fields"] = set(update_fields) | {"published_at"}
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class SiteProfile(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True, default=1, editable=False)
    site_name = models.CharField(max_length=120, default="Bitácora Robótica")
    author_name = models.CharField(max_length=150, default="Autor/a del blog")
    biography = models.TextField(
        default="Esta presentación se puede editar desde el panel de administración."
    )

    class Meta:
        verbose_name = "presentación del autor"
        verbose_name_plural = "presentación del autor"

    def __str__(self):
        return self.site_name
