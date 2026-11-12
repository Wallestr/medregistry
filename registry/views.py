from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render

from registry.models import Facility, ImmunizationRecord, Patient


def home(request):
    facilities_count = Facility.objects.filter(is_active=True).count()
    patients_count = Patient.objects.count()
    planned = ImmunizationRecord.objects.filter(
        status=ImmunizationRecord.Status.PLANNED
    ).count()
    completed = ImmunizationRecord.objects.filter(
        status=ImmunizationRecord.Status.COMPLETED
    ).count()

    recent = (
        ImmunizationRecord.objects.select_related("patient", "vaccine", "facility")
        .order_by("-planned_date", "-id")[:8]
    )
    by_region = (
        Facility.objects.filter(is_active=True)
        .values("region")
        .annotate(
            facilities=Count("id"),
            patients=Count("patients", distinct=True),
        )
        .order_by("region")
    )

    return render(
        request,
        "registry/home.html",
        {
            "facilities_count": facilities_count,
            "patients_count": patients_count,
            "planned_count": planned,
            "completed_count": completed,
            "recent": recent,
            "by_region": by_region,
        },
    )


def patient_list(request):
    q = request.GET.get("q", "").strip()
    qs = Patient.objects.select_related("facility").all()
    if q:
        qs = qs.filter(
            Q(last_name__icontains=q)
            | Q(first_name__icontains=q)
            | Q(snils__icontains=q)
        )
    return render(
        request,
        "registry/patient_list.html",
        {"patients": qs[:100], "q": q},
    )


def patient_detail(request, pk: int):
    patient = get_object_or_404(
        Patient.objects.select_related("facility"),
        pk=pk,
    )
    records = patient.immunizations.select_related("vaccine", "facility")
    return render(
        request,
        "registry/patient_detail.html",
        {"patient": patient, "records": records},
    )


def immunization_journal(request):
    status_filter = request.GET.get("status", "").strip()
    qs = ImmunizationRecord.objects.select_related(
        "patient", "vaccine", "facility"
    )
    if status_filter:
        qs = qs.filter(status=status_filter)
    return render(
        request,
        "registry/immunization_journal.html",
        {
            "records": qs[:150],
            "status_filter": status_filter,
            "statuses": ImmunizationRecord.Status.choices,
        },
    )
