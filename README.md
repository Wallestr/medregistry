# MedRegistry

Небольшой pet-проект: учёт пациентов и иммунизации на Django.

Есть HTML-страницы для просмотра журнала и REST API на DRF. База — PostgreSQL, для локального запуска можно SQLite.

## Стек

- Python 3 / Django 5 / DRF
- PostgreSQL (или SQLite)
- HTML + CSS
- Docker Compose (по желанию)

## Запуск

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

copy .env.example .env
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

- http://127.0.0.1:8000/ — интерфейс
- http://127.0.0.1:8000/api/ — API
- http://127.0.0.1:8000/admin/ — админка (`createsuperuser`)

### Через Docker

```bash
docker compose up --build
```

## Что умеет

- справочник медучреждений
- карточки пациентов
- журнал иммунизации (план / выполнено / отмена)
- API: CRUD + завершение записи (`/api/immunizations/{id}/complete/`)
- простая статистика по учреждениям (`/api/facilities/stats/`)

## Тесты

```bash
python manage.py test
```

Данные в демо вымышленные, это не боевая медсистема.
