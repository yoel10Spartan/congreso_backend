from django.urls import path
from rest_framework import routers
from apps.users.views import ExcelViewSet, UserViewSet

router = routers.SimpleRouter()

router.register(r'users', UserViewSet)
router.register(r'get_excel', ExcelViewSet)

urlpatterns = router.urls