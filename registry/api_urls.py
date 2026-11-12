from django.urls import include, path
from rest_framework.routers import DefaultRouter

from registry.api_views import (
    FacilityViewSet,
    ImmunizationRecordViewSet,
    PatientViewSet,
    VaccineViewSet,
)

router = DefaultRouter()
router.register("facilities", FacilityViewSet)
router.register("vaccines", VaccineViewSet)
router.register("patients", PatientViewSet)
router.register("immunizations", ImmunizationRecordViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
