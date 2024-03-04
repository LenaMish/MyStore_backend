from django.urls import path
from . import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="MyStore",
        default_version='v1',
        description="Description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("echo", views.echo),
    path("register", views.RegisterAPIView.as_view()),
    path("users", views.UsersListAPIView.as_view()),
    path("users/<int:pk>/delete", views.UserDestroyAPIView.as_view()),
    path("users/<int:pk>/update", views.UserUpdateAPIView.as_view()),
    path("users/<int:pk>", views.UserGetAPIView.as_view()),
    path("auth", views.AuthAPIView.as_view()),
    path("products/create", views.ProductCreateApiView.as_view(), name='product-create'),
    path("products", views.ProductListApiView.as_view()),

    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)