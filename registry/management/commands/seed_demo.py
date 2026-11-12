from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.db import transaction

from registry.models import Facility, ImmunizationRecord, Patient, Vaccine


class Command(BaseCommand):
    help = "Загружает демонстрационные данные для портфолио"

    @transaction.atomic
    def handle(self, *args, **options):
        f1, _ = Facility.objects.update_or_create(
            code="MO-001",
            defaults={
                "name": "Городская поликлиника №1",
                "facility_type": Facility.FacilityType.CLINIC,
                "region": "Тюменская область",
                "is_active": True,
            },
        )
        f2, _ = Facility.objects.update_or_create(
            code="MO-002",
            defaults={
                "name": "Областная больница",
                "facility_type": Facility.FacilityType.HOSPITAL,
                "region": "Республика Башкортостан",
                "is_active": True,
            },
        )

        vaccines = [
            ("АКДС", "V-AKDS", "Дифтерия, коклюш, столбняк"),
            ("КПК", "V-MMR", "Корь, паротит, краснуха"),
            ("Грипп", "V-FLU", "Грипп"),
        ]
        vaccine_objs = []
        for name, code, disease in vaccines:
            obj, _ = Vaccine.objects.update_or_create(
                code=code,
                defaults={"name": name, "disease": disease, "is_active": True},
            )
            vaccine_objs.append(obj)

        patients_data = [
            ("Иванов", "Иван", "Петрович", date(1990, 3, 12), "M", "123-456-789 01", f1),
            ("Петрова", "Анна", "Сергеевна", date(1985, 7, 21), "F", "123-456-789 02", f1),
            ("Сидоров", "Алексей", "Игоревич", date(2001, 11, 5), "M", "123-456-789 03", f2),
        ]
        patients = []
        for last, first, middle, birth, sex, snils, facility in patients_data:
            obj, _ = Patient.objects.update_or_create(
                snils=snils,
                defaults={
                    "last_name": last,
                    "first_name": first,
                    "middle_name": middle,
                    "birth_date": birth,
                    "sex": sex,
                    "facility": facility,
                },
            )
            patients.append(obj)

        today = date.today()
        demo_records = [
            (patients[0], vaccine_objs[0], f1, ImmunizationRecord.Status.COMPLETED, today - timedelta(days=30), today - timedelta(days=30), 1),
            (patients[0], vaccine_objs[2], f1, ImmunizationRecord.Status.PLANNED, today + timedelta(days=10), None, 1),
            (patients[1], vaccine_objs[1], f1, ImmunizationRecord.Status.COMPLETED, today - timedelta(days=90), today - timedelta(days=88), 1),
            (patients[2], vaccine_objs[0], f2, ImmunizationRecord.Status.PLANNED, today + timedelta(days=5), None, 1),
            (patients[2], vaccine_objs[2], f2, ImmunizationRecord.Status.CANCELLED, today - timedelta(days=3), None, 1),
        ]

        for patient, vaccine, facility, status, planned, performed, dose in demo_records:
            ImmunizationRecord.objects.update_or_create(
                patient=patient,
                vaccine=vaccine,
                dose_number=dose,
                defaults={
                    "facility": facility,
                    "status": status,
                    "planned_date": planned,
                    "performed_date": performed,
                    "notes": "Демо-запись",
                },
            )

        self.stdout.write(self.style.SUCCESS("Демо-данные загружены"))
