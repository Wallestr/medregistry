from rest_framework import serializers

from registry.models import Facility, ImmunizationRecord, Patient, Vaccine


class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = (
            "id",
            "name",
            "code",
            "facility_type",
            "region",
            "is_active",
            "created_at",
        )
        read_only_fields = ("id", "created_at")


class VaccineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaccine
        fields = ("id", "name", "code", "disease", "is_active")
        read_only_fields = ("id",)


class PatientSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)
    facility_name = serializers.CharField(source="facility.name", read_only=True)

    class Meta:
        model = Patient
        fields = (
            "id",
            "last_name",
            "first_name",
            "middle_name",
            "full_name",
            "birth_date",
            "sex",
            "snils",
            "facility",
            "facility_name",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at", "full_name", "facility_name")


class ImmunizationRecordSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source="patient.full_name", read_only=True)
    vaccine_name = serializers.CharField(source="vaccine.name", read_only=True)
    facility_name = serializers.CharField(source="facility.name", read_only=True)

    class Meta:
        model = ImmunizationRecord
        fields = (
            "id",
            "patient",
            "patient_name",
            "vaccine",
            "vaccine_name",
            "facility",
            "facility_name",
            "status",
            "planned_date",
            "performed_date",
            "dose_number",
            "notes",
            "created_at",
        )
        read_only_fields = (
            "id",
            "created_at",
            "patient_name",
            "vaccine_name",
            "facility_name",
        )

    def validate(self, attrs):
        status = attrs.get("status", getattr(self.instance, "status", None))
        performed = attrs.get("performed_date", getattr(self.instance, "performed_date", None))
        if status == ImmunizationRecord.Status.COMPLETED and performed is None:
            raise serializers.ValidationError(
                {"performed_date": "Для статуса «Выполнено» укажите дату выполнения."}
            )
        return attrs
