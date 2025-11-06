# Expense Tracker Django

Final version of my Expense Tracker Project. A simple web app built with Python and Django that allows users to track, manage, analyze and export their expenses. 

Users can add, edit, delete and search using filters. The app supports data export to CSV and JSON and also provides a report feature. 

---
 
## Technologies & Requirements
- Python 3.10
- Django 5.2.7

## Features

- User authentication: Login and Sign Up system.
- Expense Management: Add, edit and delete expenses.
- Search and filters: Search by category, date range or description. 
- Order: Users can order their expenses by date or amount. 
- Categories: The user can create custom categories to use in their expenses. 
- Reports: Users can generate reports filtered by category and / or date range.
- Export: Users can export their expenses list (raw or filtered) to CSV or JSON.

## Structure

expense_tracker_django/
├── manage.py
├── db.sqlite3
│
├── expense_tracker_django/      # Main project folder (settings, URLs, WSGI/ASGI)
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── tracker/                     # Core app – handles expense tracking logic
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   │
│   ├── migrations/
│   │   └── __init__.py
│   │
│   └── templates/
│       ├── base.html
│       ├── category_confirm_delete.html
│       ├── category_form.html
│       ├── category_list.html
│       ├── expense_confirm_delete.html
│       ├── expense_form.html
│       ├── expense_list.html
│       ├── reports_summary.html
│       │
│       └── registration/        # Authentication templates
│           ├── login.html
│           └── signup.html
│
└── .env                         # Environment variables (not tracked in git)

---

## Installation 

- Clone the repository
git clone <YOUR_REPO_URL>
cd expense_tracker

- Create and activate the virtual environment.
python -m venv .venv
source .venv/bin/activate 

- Install dependencies.
pip install -r requirements.txt

- Run migrations and start server
python manage.py migrate
python manage.py runserver

## How It Works

- The user registers or logs in to access the app.
- Expense list is shown with the filters above and the option to add a new expense. 
- In the navigation bar you can find the categories where you can create custom categories, and reports to generate them.
- The user can search, filter, and sort their expenses.
- Reports show total spending per category and number of transactions.
- The user can export the data to CSV or JSON. 

--- 

## What I Learned
(This was my very first Django Project ever.)
- Learned to create a basic App in Django.
- Implement an authentication system.
- Basic HTML and CSS for the templates.
- How to structuring a Django App in a simple way.

--- 
## License 
MIT © yberside. See LICENSE.
