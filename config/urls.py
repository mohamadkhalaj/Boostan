from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from config.views import food, home

urlpatterns = [
    path("", home, name="home"),
    path("food/", food, name="food"),
    path(settings.ADMIN_URL, admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# API URLS
urlpatterns += [
    # API base url
    path("api/v1/", include("api.urls")),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns

handler404 = "config.views.page_not_found_view"
handler500 = "config.views.handler500"
handler403 = "config.views.handler403"
