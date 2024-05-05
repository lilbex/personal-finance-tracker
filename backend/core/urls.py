from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
   openapi.Info(
      title="Personal Finance Tracker and Manager API",
      default_version='v1',
      description="Personal Finance Tracker and Manager API",
      terms_of_service="https://opensource.org/license/mit",
      contact=openapi.Contact(email="eliasimokhai@gmail.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(AllowAny,),
)


urlpatterns = [
    path('swagger.json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger.yaml/', schema_view.without_ui(cache_timeout=0), name='schema-yaml'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include(('authentication.urls',
         'authentication'), namespace='authentication')),
    path('api/v1/budget/', include(('budget.urls', 'budget'), namespace='budget')),
     path('api/v1/expenses/', include(('expenses.urls', 'expenses'), namespace='expenses')),
]
