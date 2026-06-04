# Ikonex Academy Student Management System
A Django-based Student Management System for Ikonex Academy. The project supports class stream management, student registration, subject assignment, score entry, grading, ranking, and printable PDF report cards.

## Features

- Class stream management
  - Create, view, edit, and delete class streams
- Student management
  - Register students and assign them to a class stream
  - View, edit, and delete student records
  - View students by class stream
- Subject management
  - Create, edit, delete, and view subjects
  - Assign subjects to class streams
- Assessment and scoring
  - Create assessments
  - Record continuous assessment and exam scores
  - Prevent duplicate score submissions
  - Validate score ranges against the assessment total
- Results processing
  - Calculate totals and averages per student
  - Apply grading scales
  - Rank students within a class stream
  - Show subject-specific class performance
- Reporting
  - View student performance summaries in the browser
  - Download individual student PDF report cards
  - Download class performance PDF reports
- Authentication and access control
  - Staff login using `staff_no` and password
  - Protected dashboards and CRUD screens
  - Account access controlled through Django staff/admin flags

## Tech Stack

- Backend: Django 6
- Frontend: HTML, CSS, Bootstrap 5, Bootstrap Icons
- Database: SQLite for local development
- PDF generation: ReportLab
- Testing: Django test framework

## Project Structure

- `accounts/` Authentication and account-related code
- `classes/` Class stream models, views, forms, and URLs
- `students/` Student management
- `subjects/` Subject management and class-subject assignment
- `assessments/` Assessments, score entry, grading, and ranking logic
- `reports/` Browser reports and PDF export views
- `templates/` Shared and app templates
- `static/` CSS, images, and JavaScript assets

## Local Setup

### 1. Create and activate a virtual environment

```bash
python -m venv env
source env/bin/activate
```

On Windows:

```bash
env\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 2a. Create your local environment file

Copy `.env.example` to `.env` and update the values for your machine.

Do not commit `.env` to git. It is already ignored.

### 3. Apply migrations

```bash
python manage.py migrate
```

This project seeds default grading bands during migration, so grades work immediately on a fresh database.

### 4. Create an admin user

```bash
python manage.py createsuperuser
```

The admin username acts as the `staff_no` used on the login screen.

### 5. Run the development server

```bash
python manage.py runserver
```

Open the app at:

```text
http://127.0.0.1:8000/
```

## Usage Guide

### Admin

- Use the sidebar to navigate between classes, students, subjects, assessments, scores, results, and reports.
- Use the Django admin panel for direct data inspection if needed:

```text
http://127.0.0.1:8000/admin/
```

### Suggested Workflow

1. Create class streams such as Form 1A, Form 1B, or Form 1C.
2. Register students and assign them to a class stream.
3. Create subjects.
4. Assign subjects to each class stream.
5. Create assessments for the term and year.
6. Enter scores for each student, subject, and assessment.
7. View results and download PDF reports.

## Grading

The system uses configurable grading bands stored in the `GradeScale` model.

Default bands are seeded automatically:

- `A` = 80-100
- `A-` = 75-79
- `B+` = 70-74
- `B` = 65-69
- `B-` = 60-64
- `C+` = 55-59
- `C` = 50-54
- `C-` = 45-49
- `D+` = 40-44
- `D` = 35-39
- `D-` = 30-34
- `E` = 0-29

## Testing

Run the full test suite with:

```bash
python manage.py test
```

The tests cover:

- Grade calculation
- Duplicate score validation
- Ranking and result aggregation

## Deployment Notes

Before deploying to production:

- Set `DEBUG = False`
- Set a secure `SECRET_KEY`
- Configure `ALLOWED_HOSTS`
- Set `DATABASE_URL` for PostgreSQL deployments, or `DATABASE_NAME` for local SQLite overrides
- Set `CSRF_TRUSTED_ORIGINS` for your production domain
- If you are using ngrok, make sure the tunnel domain is trusted by Django. The app is preconfigured for common ngrok domains, including `ngrok-free.dev`, but you can also set:

```bash
export ALLOWED_HOSTS=127.0.0.1,localhost,testserver,.ngrok-free.app,.ngrok-free.dev,.ngrok.io,.ngrok.app
export CSRF_TRUSTED_ORIGINS=https://*.ngrok-free.app,https://*.ngrok-free.dev,https://*.ngrok.io,https://*.ngrok.app
```

- Collect static files:

```bash
python manage.py collectstatic
```

- Use a production WSGI server such as Gunicorn or a platform like Railway, VPS, or Render

## Using ngrok

To expose the local app to the internet during development:

1. Start Django on your machine:

```bash
python manage.py runserver 8000
```

2. In a second terminal, start ngrok:

```bash
ngrok http 8000
```

3. Open the HTTPS forwarding URL shown by ngrok, for example:

```text
https://inbred-silverly-christeen.ngrok-free.dev
```

### Tips

- Keep `DEBUG=True` only for local development and temporary public demos.
- Because ngrok terminates HTTPS, Django should trust forwarded proto headers. This project already sets `SECURE_PROXY_SSL_HEADER` and `USE_X_FORWARDED_HOST`.
- If your ngrok URL changes, update `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` through environment variables if needed.

## Design Notes

- The interface uses a branded sidebar with the Ikonex logo on a white card for clear visibility.
- On mobile devices, the navigation collapses into an offcanvas menu for better usability.
- Tables are horizontally scrollable on small screens to avoid layout breakage.
- Result and report pages are aligned with an academic admin workflow and are suitable for school use.

## Notes

- This repository is meant for demonstration and interview review.
- If you need sample data, create it through the admin panel or the app forms.
- Staff users must be created in Django admin or via `createsuperuser`, and they should log in with their `staff_no` value.
- The app reads `.env` automatically if it exists in the project root.

## License

No license has been specified for this project.
