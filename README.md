# 📚 Library Management System

A web-based library management system built with **Python (Flask)** and **HTMX** for dynamic, no-reload interactions.

---

## Features

- **Books** — Add, edit, delete, and search books with live HTMX search
- **Members** — Manage student/member records
- **Loans** — Track book borrowing, due dates, and returns
- **Dashboard** — Overview of total books, members, active loans, and overdue books
- **Real-time UI** — HTMX-powered interactions without full page reloads
- **Flash feedback** — Inline success/error messages
- **Status filtering** — Filter loans by active, overdue, or returned
- **Loan history** — View borrowing history per book and per member

---

## Tech Stack

| Layer      | Technology                         |
|------------|------------------------------------|
| Backend    | Python 3.14, Flask                 |
| Frontend   | HTMX, Bootstrap 5, Bootstrap Icons |
| Database   | SQLite                             |
| ORM        | Flask-SQLAlchemy                   |
| Migrations | Flask-Migrate                      |
| Forms      | Flask-WTF, WTForms                 |
| Config     | python-dotenv                      |

---

## Project Structure

```
Library-Management-System/
├── app/
│   ├── __init__.py          # App factory
│   ├── config.py            # Configuration
│   ├── extensions.py        # SQLAlchemy & Migrate instances
│   ├── forms.py             # WTForms definitions
│   ├── utils.py             # Helper functions
│   ├── models/
│   │   ├── __init__.py
│   │   ├── book.py
│   │   ├── member.py
│   │   └── loan.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main.py          # Dashboard
│   │   ├── books.py
│   │   ├── members.py
│   │   └── loans.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── books/
│   │   ├── members/
│   │   ├── loans/
│   │   ├── partials/        # HTMX partial responses
│   │   └── errors/
│   └── static/
│       ├── css/style.css
│       └── js/htmx.min.js
├── instance/
│   └── library.db           # SQLite database
├── migrations/              # Flask-Migrate files
├── .env                     # Environment variables (not committed)
├── .env.example             # Environment variable template
├── .gitignore
├── requirements.txt
├── run.py
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/Kleyen/Library-Management-System.git
cd Library-Management-System

# Create and activate a virtual environment
python -m venv venv

# On Linux/Mac (fish shell)
source venv/bin/activate.fish

# On Linux/Mac (bash/zsh)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Setup

```bash
cp .env.example .env
```

Edit `.env` and set your values:
```ini
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=sqlite:///library.db
FLASK_ENV=development
FLASK_DEBUG=1
```

### Database Setup

```bash
flask --app "run:app" db init
flask --app "run:app" db migrate -m "Initial migration"
flask --app "run:app" db upgrade
```

### Running the App

```bash
python run.py
```

Visit `http://127.0.0.1:5000` in your browser.

---

## Usage

| Page      | URL          | Description                       |
|-----------|--------------|-----------------------------------|
| Dashboard | `/`          | Overview stats and recent loans   |
| Books     | `/books/`    | List, search, add, edit, delete   |
| Members   | `/members/`  | List, search, add, edit, delete   |
| Loans     | `/loans/`    | List, filter, add, return, delete |

---

## Data Models

**Book** — `title`, `author`, `isbn`, `genre`, `published_year`, `quantity`

**Member** — `student_id`, `full_name`, `email`, `phone`, `program`

**Loan** — `book_id`, `member_id`, `borrow_date`, `due_date`, `return_date`, `status`

Loan status can be: `active`, `returned`, or `overdue`

---

## Requirements

See [requirements.txt](requirements.txt) for the full list of dependencies.

---

## License

This is a personal project.