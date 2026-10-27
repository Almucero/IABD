from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, BasePermission

from .models import Article
from .serializers import ArticleSerializer


class IsActiveAdminUser(BasePermission):
    def has_permission(self, request, _view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and user.is_active
            and user.is_staff
        )


class PublishedArticleListCreateAPIView(ListCreateAPIView):
    authentication_classes = (TokenAuthentication,)
    serializer_class = ArticleSerializer

    def get_queryset(self):
        return Article.objects.filter(is_published=True)

    def get_permissions(self):
        if self.request.method == "POST":
            return (IsActiveAdminUser(),)
        return (AllowAny(),)


class PublishedArticleDetailAPIView(RetrieveAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = ArticleSerializer
    queryset = Article.objects.filter(is_published=True)
