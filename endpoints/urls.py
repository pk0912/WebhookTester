from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter
from django.views.decorators.csrf import csrf_exempt

from endpoints.views import EndpointApiView, EndpointHitApiView

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

# router.register(r"endget", EndpointViewSet, basename="endpoint")
urlpatterns = router.urls + [
    path("index/", EndpointApiView.as_view(), name="create"),
    path("<str:endpoint>/", csrf_exempt(EndpointHitApiView.as_view()), name="hit"),
]
