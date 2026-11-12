from django.contrib import admin

from registry.models import Facility, ImmunizationRecord, Patient, Vaccine


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "facility_type", "region", "is_active")
    list_filter = ("facility_type", "region", "is_active")
    search_fields = ("name", "code")


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "snils", "birth_date", "facility")
    list_filter = ("sex", "facility")
    search_fields = ("last_name", "first_name", "snils")


@admin.register(Vaccine)
class VaccineAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "disease", "is_active")
    search_fields = ("name", "code", "disease")


@admin.register(ImmunizationRecord)
class ImmunizationRecordAdmin(admin.ModelAdmin):
    list_display = (
        "patient",
        "vaccine",
        "dose_number",
        "status",
        "planned_date",
        "performed_date",
        "facility",
    )
    list_filter = ("status", "vaccine", "facility")
    search_fields = ("patient__last_name", "patient__snils", "vaccine__name")
    raw_id_fields = ("patient",)
