from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from .models import Article


class ArticleAPITests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Article.objects.all().delete()
        cls.published_article = Article.objects.create(
            title="Robótica educativa",
            slug="robotica-educativa",
            summary="Una introducción a la robótica.",
            body="Construye y aprende.",
            author="Equipo editorial",
            is_published=True,
        )
        cls.draft = Article.objects.create(
            title="Borrador interno",
            slug="borrador-interno",
            summary="No debe ser público.",
            body="Contenido privado.",
            author="Equipo editorial",
        )
        user_model = get_user_model()
        cls.admin = user_model.objects.create_user(
            username="editor",
            password="test-password",
            is_staff=True,
        )
        cls.admin_token = Token.objects.create(user=cls.admin)
        cls.reader = user_model.objects.create_user(
            username="reader",
            password="test-password",
        )
        cls.reader_token = Token.objects.create(user=cls.reader)
        cls.inactive_admin = user_model.objects.create_user(
            username="inactive-editor",
            password="test-password",
            is_staff=True,
            is_active=False,
        )
        cls.inactive_admin_token = Token.objects.create(user=cls.inactive_admin)

    def setUp(self):
        self.client = APIClient()

    def test_list_returns_only_published_articles_with_spanish_fields(self):
        response = self.client.get(reverse("api-article-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                {
                    "id": self.published_article.pk,
                    "titulo": self.published_article.title,
                    "cuerpo": self.published_article.body,
                    "estado": "publicado",
                }
            ],
        )

    def test_detail_returns_published_article_and_hides_drafts(self):
        response = self.client.get(
            reverse("api-article-detail", args=[self.published_article.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["estado"], "publicado")
        self.assertEqual(response.json()["titulo"], self.published_article.title)

        for article_id in (self.draft.pk, self.published_article.pk + 100):
            with self.subTest(article_id=article_id):
                hidden_response = self.client.get(
                    reverse("api-article-detail", args=[article_id])
                )
                self.assertEqual(hidden_response.status_code, 404)

    def test_admin_token_creates_private_draft_and_web_regression_holds(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.admin_token.key}"
        )
        response = self.client.post(
            reverse("api-article-list"),
            {"titulo": "Robot de aula", "cuerpo": "Prueba\ndidáctica."},
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        created = Article.objects.get(pk=response.json()["id"])
        self.assertEqual(
            response.json(),
            {
                "id": created.pk,
                "titulo": "Robot de aula",
                "cuerpo": "Prueba\ndidáctica.",
                "estado": "borrador",
            },
        )
        self.assertFalse(created.is_published)
        self.assertEqual(created.summary, "Prueba\ndidáctica.")
        self.assertEqual(created.author, self.admin.get_username())
        self.assertNotContains(
            self.client.get(reverse("home")),
            "Robot de aula",
        )
        self.assertNotIn(
            created.pk,
            [article["id"] for article in self.client.get(
                reverse("api-article-list")
            ).json()],
        )

    def test_api_generates_a_unique_slug_for_repeated_titles(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.admin_token.key}"
        )
        url = reverse("api-article-list")
        payload = {"titulo": "Un mismo título", "cuerpo": "Texto"}

        first_response = self.client.post(url, payload, format="json")
        second_response = self.client.post(url, payload, format="json")

        self.assertEqual(first_response.status_code, 201)
        self.assertEqual(second_response.status_code, 201)
        first_article = Article.objects.get(pk=first_response.json()["id"])
        second_article = Article.objects.get(pk=second_response.json()["id"])
        self.assertNotEqual(first_article.slug, second_article.slug)

    def test_post_requires_an_admin_token(self):
        post_data = {"titulo": "Nuevo robot", "cuerpo": "Texto"}

        anonymous_response = self.client.post(
            reverse("api-article-list"), post_data, format="json"
        )
        self.assertEqual(anonymous_response.status_code, 401)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.reader_token.key}"
        )
        reader_response = self.client.post(
            reverse("api-article-list"), post_data, format="json"
        )
        self.assertEqual(reader_response.status_code, 403)

        self.client.credentials(HTTP_AUTHORIZATION="Token invalid-token")
        invalid_token_response = self.client.post(
            reverse("api-article-list"), post_data, format="json"
        )
        self.assertEqual(invalid_token_response.status_code, 401)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.inactive_admin_token.key}"
        )
        inactive_admin_response = self.client.post(
            reverse("api-article-list"), post_data, format="json"
        )
        self.assertIn(inactive_admin_response.status_code, (401, 403))
        self.assertFalse(Article.objects.filter(title="Nuevo robot").exists())

    def test_post_rejects_missing_or_blank_required_fields(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.admin_token.key}"
        )
        initial_count = Article.objects.count()

        for post_data in (
            {"cuerpo": "Falta el título"},
            {"titulo": "Falta el cuerpo"},
            {"titulo": "   ", "cuerpo": "Texto"},
            {"titulo": "Cuerpo vacío", "cuerpo": "   "},
        ):
            with self.subTest(post_data=post_data):
                response = self.client.post(
                    reverse("api-article-list"), post_data, format="json"
                )
                self.assertEqual(response.status_code, 400)

        self.assertEqual(Article.objects.count(), initial_count)
