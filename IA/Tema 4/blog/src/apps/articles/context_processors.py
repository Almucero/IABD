from .models import Category


def published_categories(request):
    return {
        "published_categories": Category.objects.filter(
            articles__is_published=True
        ).distinct()
    }
