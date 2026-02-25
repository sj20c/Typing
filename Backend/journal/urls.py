from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HappyMomentViewSet, WeeklyReportView

router = DefaultRouter()
router.register(r"moments", HappyMomentViewSet, basename="moments")

urlpatterns = [
    path("", include(router.urls)),
    path("reports/weekly", WeeklyReportView.as_view()),
]
