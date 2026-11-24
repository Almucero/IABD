from datetime import timedelta
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Article, SiteProfile


class PublicBlogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Article.objects.all().delete()
        now = timezone.now()
        cls.older_article = Article.objects.create(
            title="Sensores para empezar",
            slug="sensores-para-empezar",
            summary="Una guía introductoria a los sensores.",
            body=(
                "Los sensores ayudan a un robot a percibir su entorno.\n\n"
                "## Elegir un sensor\n\n"
                "Empieza por definir qué dato necesita medir el proyecto."
            ),
            author="Alex Robótica",
            published_at=now - timedelta(days=1),
            is_published=True,
        )
        cls.newer_article = Article.objects.create(
            title="Un brazo robótico sencillo",
            slug="brazo-robotico-sencillo",
            summary="Conoce las partes básicas de un brazo robótico.",
            body="Un proyecto para aprender sobre movimiento.",
            author="Alex Robótica",
            published_at=now,
            is_published=True,
        )
        cls.draft = Article.objects.create(
            title="Borrador privado",
            slug="borrador-privado",
            summary="Todavía no está listo.",
            body="Texto de un borrador que no debe ser público.",
            author="Alex Robótica",
        )

    def test_home_shows_published_articles_in_date_order(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["articles"]),
            [self.newer_article, self.older_article],
        )
        self.assertContains(response, self.older_article.title)
        self.assertContains(response, self.older_article.summary)
        self.assertContains(response, self.older_article.author)
        self.assertContains(
            response,
            reverse("article-detail", kwargs={"slug": self.older_article.slug}),
        )
        self.assertNotContains(response, self.draft.title)

    def test_empty_home_has_an_informative_message(self):
        Article.objects.all().delete()

        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Aún no hay artículos publicados")

    def test_published_article_shows_author_date_paragraphs_and_subheadings(self):
        response = self.client.get(
            reverse("article-detail", kwargs={"slug": self.older_article.slug})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.older_article.title)
        self.assertContains(response, self.older_article.author)
        self.assertContains(response, self.older_article.published_at.strftime("%Y"))
        self.assertContains(response, "<h2>Elegir un sensor</h2>", html=True)
        self.assertContains(response, "Los sensores ayudan a un robot")

    def test_article_body_escapes_html_instead_of_rendering_user_markup(self):
        self.older_article.body = "<script>alert('x')</script>"
        self.older_article.save()

        response = self.client.get(
            reverse("article-detail", kwargs={"slug": self.older_article.slug})
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "<script>")
        self.assertContains(response, "&lt;script&gt;")

    def test_unpublished_and_missing_articles_return_404(self):
        for slug in (self.draft.slug, "no-existe"):
            with self.subTest(slug=slug):
                response = self.client.get(
                    reverse("article-detail", kwargs={"slug": slug})
                )
                self.assertEqual(response.status_code, 404)
                self.assertNotContains(
                    response,
                    self.draft.body,
                    status_code=404,
                )

    def test_navigation_links_home_and_about_from_public_pages(self):
        detail_response = self.client.get(
            reverse("article-detail", kwargs={"slug": self.older_article.slug})
        )
        about_response = self.client.get(reverse("about"))

        self.assertContains(detail_response, reverse("home"))
        self.assertContains(detail_response, reverse("about"))
        self.assertEqual(about_response.status_code, 200)
        self.assertContains(about_response, reverse("home"))
        self.assertContains(about_response, reverse("about"))
        self.assertContains(about_response, "Sobre mí")

    def test_about_page_uses_editable_profile(self):
        profile = SiteProfile.objects.get(pk=1)
        profile.author_name = "Roberta Inventora"
        profile.biography = "Me interesa compartir proyectos de robótica."
        profile.save()

        response = self.client.get(reverse("about"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Roberta Inventora")
        self.assertContains(response, "compartir proyectos de robótica")

    def test_there_is_no_public_registration_route(self):
        response = self.client.get("/accounts/register/")

        self.assertEqual(response.status_code, 404)

    def test_article_publication_has_true_and_false_boolean_states(self):
        publication_field = Article._meta.get_field("is_published")

        self.assertIsInstance(publication_field, models.BooleanField)
        self.assertFalse(self.draft.is_published)
        self.assertTrue(self.older_article.is_published)

    def test_publishing_without_a_date_assigns_the_current_time(self):
        article = Article.objects.create(
            title="Publicación con fecha automática",
            slug="publicacion-con-fecha-automatica",
            summary="Una prueba de publicación.",
            body="Contenido de prueba.",
            author="Alex Robótica",
        )

        article.is_published = True
        article.save(update_fields=["is_published"])
        article.refresh_from_db()
        self.assertIsNotNone(article.published_at)

    def test_robotics_image_is_stored_under_the_configured_media_directory(self):
        image_path = Path(settings.MEDIA_ROOT) / "images" / "robot-orbit.svg"

        self.assertTrue(image_path.is_file())


class ArticleAdminTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.article = Article.objects.create(
            title="Prueba de sensores",
            slug="prueba-de-sensores",
            summary="Una práctica de robótica.",
            body="Contenido del artículo.",
            author="Alex Robótica",
        )
        get_user_model().objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="test-password",
        )

    def setUp(self):
        self.client.force_login(get_user_model().objects.get(username="admin"))

    def test_admin_can_search_and_edit_articles(self):
        response = self.client.get(
            reverse("admin:articles_article_changelist"),
            {"q": self.article.title},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.article.title)
        self.assertContains(response, self.article.author)

        response = self.client.post(
            reverse("admin:articles_article_change", args=[self.article.pk]),
            {
                "title": "Prueba de sensores actualizada",
                "slug": self.article.slug,
                "summary": "Resumen actualizado.",
                "body": "Contenido revisado.",
                "author": "Roberta Inventora",
                "_save": "Guardar",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.article.refresh_from_db()
        self.assertEqual(self.article.title, "Prueba de sensores actualizada")
        self.assertEqual(self.article.author, "Roberta Inventora")

    def test_admin_can_create_and_delete_articles(self):
        response = self.client.post(
            reverse("admin:articles_article_add"),
            {
                "title": "Nuevo proyecto",
                "slug": "nuevo-proyecto",
                "summary": "Resumen del proyecto.",
                "body": "Contenido del proyecto.",
                "author": "Alex Robótica",
                "_save": "Guardar",
            },
        )

        self.assertEqual(response.status_code, 302)
        article = Article.objects.get(slug="nuevo-proyecto")

        response = self.client.post(
            reverse("admin:articles_article_delete", args=[article.pk]),
            {"post": "yes"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Article.objects.filter(pk=article.pk).exists())

    def test_admin_can_update_author_presentation(self):
        response = self.client.post(
            reverse("admin:articles_siteprofile_change", args=[1]),
            {
                "site_name": "Robótica abierta",
                "author_name": "Alex Robótica",
                "biography": "Comparto lo que aprendo construyendo robots.",
                "_save": "Guardar",
            },
        )

        self.assertEqual(response.status_code, 302)
        profile = SiteProfile.objects.get(pk=1)
        self.assertEqual(profile.site_name, "Robótica abierta")
        self.assertEqual(profile.author_name, "Alex Robótica")

    def test_anonymous_user_cannot_access_admin(self):
        self.client.logout()

        response = self.client.get(reverse("admin:articles_article_changelist"))

        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login/", response.url)
