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

### 3. Apply migrations

```bash
python manage.py migrate
```

This project seeds default grading bands during migration, so grades work immediately on a fresh database.

### 4. Create an admin user

```bash
python manage.py createsuperuser
```

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
- Replace SQLite with PostgreSQL or MySQL
- Collect static files:

```bash
python manage.py collectstatic
```

- Use a production WSGI server such as Gunicorn or a platform like Railway, VPS, or Render

## Design Notes

- The interface uses a branded sidebar with the Ikonex logo on a white card for clear visibility.
- On mobile devices, the navigation collapses into an offcanvas menu for better usability.
- Tables are horizontally scrollable on small screens to avoid layout breakage.
- Result and report pages are aligned with an academic admin workflow and are suitable for school use.

## Notes

- This repository is meant for demonstration and interview review.
- If you need sample data, create it through the admin panel or the app forms.

## License

No license has been specified for this project.
