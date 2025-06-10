# 💸 Django Expense Tracker

A personal expense tracking web app built with Django. It lets users log their expenses, categorize them, set monthly budgets, and view detailed reports and charts.

---

## 🚀 Features

- ✅ User authentication (login/register)
- 📋 Add, edit, delete expenses
- 💰 Set monthly budgets per user
- 📊 Filter reports (weekly, monthly, yearly, custom)
- 🧾 Charts (pie and line charts) using Chart.js
- 📈 Detect recurring expenses
- 📅 Date-range filtering with automatic summaries

---

## 🛠 Tech Stack

- **Backend:** Django 4.x
- **Frontend:** HTML5, Bootstrap 5, Chart.js
- **Database:** SQLite (default), PostgreSQL (production-ready)
- **Others:** Django messages framework, custom forms, date parsing

---

## 📦 Installation

### 1. Clone the repo

```bash
git clone https://github.com/karmakr1920/expense_tracker.git
cd expense-tracker
````

### 2. Set up virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Create a superuser (admin)

```bash
python manage.py createsuperuser
```

### 6. Run the server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

---

## ✏️ Usage Guide

* Register and log in as a user.
* Go to your dashboard:

  * Add new expenses with category and amount.
  * View total and remaining budget for the current month.
* Set or update your monthly budget.
* Go to the **Report** section:

  * Filter expenses by weekly, monthly, yearly, or custom range.
  * View charts and recurring expense patterns.

---

## 🧾 Project Structure

```
expense_tracker/
├── tracker/            # Main app: models, views, templates
│   ├── templates/
│   ├── static/
│   └── ...
├── db.sqlite3          # Default dev database
├── manage.py
├── requirements.txt
└── README.md
```

## 📝 License

MIT License. Feel free to fork and improve.

---

## 🙌 Contributions

PRs are welcome! Feel free to file issues or feature requests.

Feel Free to connect me on Linkedin
https://www.linkedin.com/in/navin-kumar-550377223/