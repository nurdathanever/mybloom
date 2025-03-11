from django.contrib import admin
from django.urls import path, include
from .views import home, catalog
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("", home, name="home"),
    path("catalog/", catalog, name="catalog"),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("accounts/", include("accounts.urls")),
    path("i18n/", include("django.conf.urls.i18n")),
    path("products/", include("products.urls")),
    path("admin-dashboard/", include("admin_panel.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)