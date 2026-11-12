from django.db.models import Count, Q
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from registry.models import Facility, ImmunizationRecord, Patient, Vaccine
from registry.serializers import (
    FacilitySerializer,
    ImmunizationRecordSerializer,
    PatientSerializer,
    VaccineSerializer,
)


class FacilityViewSet(viewsets.ModelViewSet):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer

    def get_queryset(self):
        qs = super().get_queryset()
        region = self.request.query_params.get("region")
        facility_type = self.request.query_params.get("facility_type")
        if region:
            qs = qs.filter(region__icontains=region)
        if facility_type:
            qs = qs.filter(facility_type=facility_type)
        return qs

    @action(detail=False, methods=["get"], url_path="stats")
    def stats(self, request):
        """Сводная статистика по учреждениям — пример агрегации SQL через ORM."""
        rows = (
            Facility.objects.filter(is_active=True)
            .annotate(
                patients_count=Count("patients", distinct=True),
                completed_immunizations=Count(
                    "immunizations",
                    filter=Q(immunizations__status=ImmunizationRecord.Status.COMPLETED),
                    distinct=True,
                ),
                planned_immunizations=Count(
                    "immunizations",
                    filter=Q(immunizations__status=ImmunizationRecord.Status.PLANNED),
                    distinct=True,
                ),
            )
            .values(
                "id",
                "name",
                "code",
                "region",
                "patients_count",
                "completed_immunizations",
                "planned_immunizations",
            )
            .order_by("region", "name")
        )
        return Response(list(rows))


class VaccineViewSet(viewsets.ModelViewSet):
    queryset = Vaccine.objects.all()
    serializer_class = VaccineSerializer


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.select_related("facility").all()
    serializer_class = PatientSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.query_params.get("q")
        facility_id = self.request.query_params.get("facility")
        if q:
            qs = qs.filter(
                Q(last_name__icontains=q)
                | Q(first_name__icontains=q)
                | Q(snils__icontains=q)
            )
        if facility_id:
            qs = qs.filter(facility_id=facility_id)
        return qs


class ImmunizationRecordViewSet(viewsets.ModelViewSet):
    queryset = ImmunizationRecord.objects.select_related(
        "patient", "vaccine", "facility"
    ).all()
    serializer_class = ImmunizationRecordSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        status_param = self.request.query_params.get("status")
        patient_id = self.request.query_params.get("patient")
        if status_param:
            qs = qs.filter(status=status_param)
        if patient_id:
            qs = qs.filter(patient_id=patient_id)
        return qs

    @action(detail=True, methods=["post"], url_path="complete")
    def complete(self, request, pk=None):
        record = self.get_object()
        performed_date = request.data.get("performed_date")
        if not performed_date:
            return Response(
                {"detail": "Укажите performed_date"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        record.status = ImmunizationRecord.Status.COMPLETED
        record.performed_date = performed_date
        record.save(update_fields=["status", "performed_date"])
        return Response(self.get_serializer(record).data)
