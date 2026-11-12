# MedRegistry

Демо-модуль медицинской информационной системы: учёт пациентов и иммунизации.

Сделан как обсуждаемый на собеседовании GitHub-проект под вакансии вроде КОМТЕК (Python + PostgreSQL + веб/REST, плюс Django/DRF и HTML).

## Стек

- Python 3.12
- Django 5 + Django REST Framework
- PostgreSQL (SQLite для быстрого локального старта)
- HTML/CSS шаблоны (обзор, пациенты, журнал)
- Docker Compose

## Что внутри

| Слой | Возможности |
|------|-------------|
| Модели | учреждения, пациенты, вакцины, факты иммунизации, ограничения уникальности дозы |
| REST API | CRUD + `POST /api/immunizations/{id}/complete/` + `GET /api/facilities/stats/` |
| HTML | дашборд, поиск пациентов, карточка, журнал со статусами |
| SQL/ORM | фильтры, `annotate`/`Count`, индексы, `PROTECT`/`CASCADE` |

Домен упрощённый (учебный), но близкий к реальным задачам: справочники МО, карточка пациента, журнал вакцинации, API для смежных систем.

## Быстрый старт (SQLite)

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
pip install -r requirements.txt

copy .env.example .env
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

Открыть:

- UI: http://127.0.0.1:8000/
- API: http://127.0.0.1:8000/api/
- Admin: http://127.0.0.1:8000/admin/ (`createsuperuser` при необходимости)

## PostgreSQL через Docker

```bash
docker compose up --build
```

UI/API на http://localhost:8000/

## Тесты

```bash
python manage.py test
```

## Примеры API

```bash
# пациенты
curl http://127.0.0.1:8000/api/patients/

# статистика по учреждениям
curl http://127.0.0.1:8000/api/facilities/stats/

# завершить вакцинацию
curl -X POST http://127.0.0.1:8000/api/immunizations/1/complete/ \
  -H "Content-Type: application/json" \
  -d "{\"performed_date\": \"2026-12-02\"}"
```

## О чём говорить на собеседовании

1. Почему `PROTECT` на учреждении/вакцине и `CASCADE` на записях пациента.
2. Зачем constraint `uniq_patient_vaccine_dose`.
3. Как устроен action `complete` и валидация статуса в serializer.
4. Как `facilities/stats` считает агрегаты без сырого SQL (и где сырой SQL был бы уместен).
5. Разделение HTML UI и REST API в одном Django-проекте.

## Важно

Это портфолио-демо, не клинический продукт. Персональные данные — вымышленные.
