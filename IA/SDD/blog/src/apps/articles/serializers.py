from uuid import uuid4

from django.db import transaction
from django.utils.text import slugify
from rest_framework import serializers

from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    titulo = serializers.CharField(source="title", max_length=200)
    cuerpo = serializers.CharField(source="body", trim_whitespace=False)
    estado = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ("id", "titulo", "cuerpo", "estado")
        read_only_fields = ("id", "estado")

    def validate_cuerpo(self, value):
        if not value.strip():
            raise serializers.ValidationError("El cuerpo no puede estar vacío.")
        return value

    def get_estado(self, article):
        return "publicado" if article.is_published else "borrador"

    @transaction.atomic
    def create(self, validated_data):
        title = validated_data["title"]
        body = validated_data["body"]
        base_slug = (slugify(title) or "articulo")[:180].rstrip("-") or "articulo"
        article = Article.objects.create(
            title=title,
            slug=f"api-draft-{uuid4().hex}",
            summary=body.strip()[:300],
            body=body,
            author=self.context["request"].user.get_username(),
            is_published=False,
        )
        article.slug = f"{base_slug}-{article.pk}"
        article.save(update_fields=["slug"])
        return article
