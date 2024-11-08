"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("apps.Users.urls")),
    path("investment/", include("apps.investment.urls")),
    path("dresses/", include("apps.Dresses.urls")),
    path("CustomerReviews/", include("apps.CustomerReviews.urls")),
    path("Cart/", include("apps.Cart.urls")),
    path("FAQ_and_terms/", include("apps.FAQ_and_terms.urls")),
    path("orders/", include("apps.orders.urls")),
    path("Payment/", include("apps.Payment.urls")),
    path("invitation/", include("apps.invitation.urls")),
    path("Dashboard/", include("apps.Dashboard.urls")),
    # path('tinymce/', include('tinymce.urls')),
    path("captcha/", include("captcha.urls")),
    path("Captcha_ap/", include("apps.Captcha_app.urls")),
    path("ckeditor5/", include("django_ckeditor_5.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
