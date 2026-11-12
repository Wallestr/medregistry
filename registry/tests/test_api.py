from datetime import date

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from registry.models import Facility, ImmunizationRecord, Patient, Vaccine


class ApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.facility = Facility.objects.create(
            name="Тестовая поликлиника",
            code="T-001",
            facility_type=Facility.FacilityType.CLINIC,
            region="Тюменская область",
        )
        self.vaccine = Vaccine.objects.create(
            name="Грипп",
            code="FLU",
            disease="Грипп",
        )
        self.patient = Patient.objects.create(
            last_name="Тестов",
            first_name="Тест",
            birth_date=date(1995, 1, 1),
            sex=Patient.Sex.MALE,
            snils="111-222-333 44",
            facility=self.facility,
        )

    def test_create_immunization_and_complete(self):
        create_url = reverse("immunizationrecord-list")
        payload = {
            "patient": self.patient.id,
            "vaccine": self.vaccine.id,
            "facility": self.facility.id,
            "status": "planned",
            "planned_date": "2026-12-01",
            "dose_number": 1,
        }
        response = self.client.post(create_url, payload, format="json")
        self.assertEqual(response.status_code, 201, response.content)
        record_id = response.data["id"]

        complete_url = reverse("immunizationrecord-complete", args=[record_id])
        done = self.client.post(
            complete_url,
            {"performed_date": "2026-12-02"},
            format="json",
        )
        self.assertEqual(done.status_code, 200, done.content)
        self.assertEqual(done.data["status"], "completed")

        record = ImmunizationRecord.objects.get(pk=record_id)
        self.assertEqual(record.status, ImmunizationRecord.Status.COMPLETED)

    def test_facility_stats(self):
        ImmunizationRecord.objects.create(
            patient=self.patient,
            vaccine=self.vaccine,
            facility=self.facility,
            status=ImmunizationRecord.Status.COMPLETED,
            planned_date=date(2026, 1, 10),
            performed_date=date(2026, 1, 10),
            dose_number=1,
        )
        url = reverse("facility-stats")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(any(row["code"] == "T-001" for row in response.data))

    def test_patient_search_page(self):
        response = self.client.get(reverse("patient_list"), {"q": "Тестов"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Тестов")
