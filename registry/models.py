from django.db import models
from django.db.models import Q


class Facility(models.Model):
    """Медицинское учреждение (поликлиника / стационар)."""

    class FacilityType(models.TextChoices):
        CLINIC = "clinic", "Поликлиника"
        HOSPITAL = "hospital", "Стационар"
        OTHER = "other", "Прочее"

    name = models.CharField("Наименование", max_length=255)
    code = models.CharField("Код МО", max_length=32, unique=True)
    facility_type = models.CharField(
        "Тип",
        max_length=32,
        choices=FacilityType.choices,
        default=FacilityType.CLINIC,
    )
    region = models.CharField("Регион", max_length=128)
    is_active = models.BooleanField("Активно", default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Учреждение"
        verbose_name_plural = "Учреждения"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["region", "is_active"]),
        ]

    def __str__(self) -> str:
        return f"{self.name} ({self.code})"


class Patient(models.Model):
    """Пациент — базовая карточка для диспансерного учёта / иммунизации."""

    class Sex(models.TextChoices):
        MALE = "M", "Мужской"
        FEMALE = "F", "Женский"

    last_name = models.CharField("Фамилия", max_length=100)
    first_name = models.CharField("Имя", max_length=100)
    middle_name = models.CharField("Отчество", max_length=100, blank=True)
    birth_date = models.DateField("Дата рождения")
    sex = models.CharField("Пол", max_length=1, choices=Sex.choices)
    snils = models.CharField("СНИЛС", max_length=14, unique=True)
    facility = models.ForeignKey(
        Facility,
        on_delete=models.PROTECT,
        related_name="patients",
        verbose_name="Учреждение прикрепления",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Пациент"
        verbose_name_plural = "Пациенты"
        ordering = ["last_name", "first_name"]
        indexes = [
            models.Index(fields=["last_name", "first_name"]),
            models.Index(fields=["birth_date"]),
        ]

    def __str__(self) -> str:
        return f"{self.last_name} {self.first_name} ({self.snils})"

    @property
    def full_name(self) -> str:
        parts = [self.last_name, self.first_name, self.middle_name]
        return " ".join(p for p in parts if p)


class Vaccine(models.Model):
    """Справочник вакцин / препаратов для иммунизации."""

    name = models.CharField("Название", max_length=255)
    code = models.CharField("Код", max_length=64, unique=True)
    disease = models.CharField("Инфекция / показание", max_length=255)
    is_active = models.BooleanField("Активна", default=True)

    class Meta:
        verbose_name = "Вакцина"
        verbose_name_plural = "Вакцины"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class ImmunizationRecord(models.Model):
    """Факт иммунизации — событие учёта."""

    class Status(models.TextChoices):
        PLANNED = "planned", "Запланировано"
        COMPLETED = "completed", "Выполнено"
        CANCELLED = "cancelled", "Отменено"

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="immunizations",
        verbose_name="Пациент",
    )
    vaccine = models.ForeignKey(
        Vaccine,
        on_delete=models.PROTECT,
        related_name="records",
        verbose_name="Вакцина",
    )
    facility = models.ForeignKey(
        Facility,
        on_delete=models.PROTECT,
        related_name="immunizations",
        verbose_name="Место проведения",
    )
    status = models.CharField(
        "Статус",
        max_length=16,
        choices=Status.choices,
        default=Status.PLANNED,
        db_index=True,
    )
    planned_date = models.DateField("Плановая дата")
    performed_date = models.DateField("Дата выполнения", null=True, blank=True)
    dose_number = models.PositiveSmallIntegerField("Номер дозы", default=1)
    notes = models.TextField("Примечание", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Иммунизация"
        verbose_name_plural = "Иммунизации"
        ordering = ["-planned_date", "-id"]
        constraints = [
            models.UniqueConstraint(
                fields=["patient", "vaccine", "dose_number"],
                name="uniq_patient_vaccine_dose",
            ),
            models.CheckConstraint(
                condition=Q(dose_number__gte=1),
                name="dose_number_positive",
            ),
        ]
        indexes = [
            models.Index(fields=["status", "planned_date"]),
        ]

    def __str__(self) -> str:
        return f"{self.patient} — {self.vaccine} (доза {self.dose_number})"
