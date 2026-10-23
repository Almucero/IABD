from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Article, Category


class PublicArticleViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name="Cuidados", slug="cuidados")
        cls.older_article = Article.objects.create(
            title="Primeros pasos",
            slug="primeros-pasos",
            summary="Una guía para empezar.",
            body="Contenido del artículo.",
            category=cls.category,
            published_at=timezone.now() - timedelta(days=1),
            is_published=True,
        )
        cls.newer_article = Article.objects.create(
            title="Agua limpia",
            slug="agua-limpia",
            summary="Consejos de mantenimiento.",
            body="Más contenido.",
            category=cls.category,
            published_at=timezone.now(),
            is_published=True,
        )
        cls.draft = Article.objects.create(
            title="Borrador privado",
            slug="borrador-privado",
            summary="No debe mostrarse.",
            body="Contenido privado.",
            category=cls.category,
        )
        cls.other_category = Category.objects.create(
            name="Alimentación",
            slug="alimentacion",
        )
        cls.other_category_article = Article.objects.create(
            title="Comida adecuada",
            slug="comida-adecuada",
            summary="Consejos de alimentación.",
            body="Contenido sobre alimentación.",
            category=cls.other_category,
            published_at=timezone.now() - timedelta(days=2),
            is_published=True,
        )

    def test_home_shows_published_articles_newest_first(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["articles"]),
            [self.newer_article, self.older_article, self.other_category_article],
        )
        self.assertContains(response, self.older_article.title)
        self.assertContains(response, self.older_article.summary)
        self.assertContains(response, self.category.name)
        self.assertContains(
            response,
            reverse("article-detail", kwargs={"slug": self.older_article.slug}),
        )
        self.assertNotContains(response, self.draft.title)

    def test_category_page_only_shows_published_articles(self):
        response = self.client.get(
            reverse("category-detail", kwargs={"slug": self.category.slug})
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["articles"]), 2)
        self.assertNotContains(response, self.draft.title)
        self.assertNotContains(response, self.other_category_article.title)
        self.assertContains(response, reverse("home"))
        self.assertContains(response, reverse("category-detail", kwargs={"slug": "cuidados"}))

    def test_published_article_detail_shows_content_and_navigation(self):
        response = self.client.get(
            reverse("article-detail", kwargs={"slug": self.newer_article.slug})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.newer_article.title)
        self.assertContains(response, self.newer_article.body)
        self.assertContains(response, self.category.name)
        self.assertContains(response, reverse("home"))
        self.assertContains(
            response,
            reverse("category-detail", kwargs={"slug": self.category.slug}),
        )

    def test_unpublished_article_detail_returns_404_without_content(self):
        response = self.client.get(
            reverse("article-detail", kwargs={"slug": self.draft.slug})
        )

        self.assertEqual(response.status_code, 404)
        self.assertNotContains(response, self.draft.body, status_code=404)


class ArticleAdminTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name="Cuidados", slug="cuidados")
        cls.article = Article.objects.create(
            title="Primeros pasos",
            slug="primeros-pasos",
            summary="Una guía para empezar.",
            body="Contenido inicial.",
            category=cls.category,
        )
        get_user_model().objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="test-password",
        )

    def setUp(self):
        self.client.force_login(
            get_user_model().objects.get(username="admin")
        )

    def test_article_admin_lists_category_publication_status_and_searches_title(self):
        response = self.client.get(
            reverse("admin:articles_article_changelist"),
            {"q": self.article.title},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.article.title)
        self.assertContains(response, self.category.name)
        self.assertContains(response, "No")

    def test_admin_can_create_and_edit_category_and_article(self):
        category_add_url = reverse("admin:articles_category_add")
        response = self.client.post(
            category_add_url,
            {"name": "Alimentación", "slug": "alimentacion", "_save": "Guardar"},
        )
        self.assertEqual(response.status_code, 302)
        category = Category.objects.get(slug="alimentacion")

        response = self.client.post(
            reverse("admin:articles_category_change", args=[category.pk]),
            {"name": "Nutrición", "slug": "nutricion", "_save": "Guardar"},
        )
        self.assertEqual(response.status_code, 302)
        category.refresh_from_db()
        self.assertEqual(category.name, "Nutrición")

        article_add_url = reverse("admin:articles_article_add")
        response = self.client.post(
            article_add_url,
            {
                "title": "Alimentación equilibrada",
                "slug": "alimentacion-equilibrada",
                "summary": "Una pauta básica.",
                "body": "Contenido del artículo.",
                "category": category.pk,
                "_save": "Guardar",
            },
        )
        self.assertEqual(response.status_code, 302)
        article = Article.objects.get(slug="alimentacion-equilibrada")

        response = self.client.post(
            reverse("admin:articles_article_change", args=[article.pk]),
            {
                "title": "Alimentación adecuada",
                "slug": article.slug,
                "summary": "Una pauta actualizada.",
                "body": "Contenido actualizado.",
                "category": category.pk,
                "_save": "Guardar",
            },
        )
        self.assertEqual(response.status_code, 302)
        article.refresh_from_db()
        self.assertEqual(article.title, "Alimentación adecuada")
        self.assertEqual(article.summary, "Una pauta actualizada.")
