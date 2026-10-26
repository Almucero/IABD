from .models import SiteProfile


def site_profile(request):
    return {"site_profile": SiteProfile.objects.filter(pk=1).first()}
