# Water Refill Station

A Django web application built to manage day-to-day operations for a water refilling business that sells 1L, 5L, 10L, and 20L containers. This project is based on a real business I run, and is being developed as a structured, four-week portfolio build.

The goal is to move the business from manual tracking to a proper system that handles customers, sales, credit/debt, stock, and eventually delivery and tank-level monitoring.

## Motivation

I run a water refilling shop and wanted to solve a real operational problem: tracking who owes money, knowing when stock is low, and eventually being able to message customers directly about debts, shop hours, or promotions. Rather than build a generic tutorial project, this app is shaped around the actual day-to-day needs of the business.

## Tech Stack

- **Backend:** Django 5.2
- **Database:** PostgreSQL 16
- **Frontend:** Bootstrap 5.3
- **Environment management:** python-decouple (for `.env` based configuration)
- **API (planned):** Django REST Framework, for the tank-level monitoring endpoint and future integrations
- **SMS (planned):** Africa's Talking API, for customer messaging and debt reminders

## Project Status

This project is being built over four weeks. Current progress:

- [x] Project setup, virtual environment, and PostgreSQL connection
- [x] Bootstrap base layout with sidebar navigation
- [ ] Customer model and management (in progress)
- [ ] Product model and stock tracking
- [ ] Sales recording with credit/debt tracking
- [ ] Dashboard with daily sales summary
- [ ] SMS integration for customer messaging
- [ ] Tank level monitoring (software-first, hardware integration later)
- [ ] Authentication and deployment

## Planned Features

**Customer management**
Track customers, including those who pay on credit, and identify who currently owes money.

**Product management**
Manage the four container sizes, their prices, and stock levels.

**Sales tracking**
Record sales, calculate totals automatically, and flag whether a sale was paid or is outstanding.

**Customer messaging**
Filter customers who are in debt and send them a customized message, for example about shop hours over the holidays or available discounts. Built using the Africa's Talking SMS API.

**Tank level monitoring**
Track water tank levels so the shop owner knows when stock is running low and a refill needs to be arranged. The system is designed so that tank readings can initially be entered manually or via a script, and later replaced with real sensor hardware (ultrasonic sensor and a WiFi-enabled microcontroller) without changing the underlying application.

## Local Setup

These instructions assume macOS with Homebrew.

### Prerequisites

- Python 3.10+
- PostgreSQL 16
- Git

### Installation

Clone the repository:

```bash
git clone git@github.com:feliciaomollo/Water_Refill_Station.git
cd water_shop
```

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install django psycopg2-binary python-decouple djangorestframework
```

Create a `.env` file in the project root with the following variables:

```
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=water_shop_db
DB_USER=your-postgres-username
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=5432
```

Create the PostgreSQL database:

```bash
createdb water_shop_db
```

Run migrations:

```bash
python manage.py migrate
```

Start the development server:

```bash
python manage.py runserver
```

The app will be available at `http://127.0.0.1:8000/`.

## Project Structure

```
water_shop/
├── core/           # Project configuration (settings, URLs, WSGI)
├── shop/           # Main application (models, views, templates)
│   ├── templates/shop/
│   └── static/shop/
├── manage.py
├── .env            # Not committed; holds local secrets and DB credentials
└── .gitignore
```

## Development Workflow

This project follows a feature-branch workflow:

1. Create a branch for each feature (e.g. `feature/customer-model`)
2. Commit work incrementally with descriptive messages
3. Push the branch and open a pull request into `main`
4. Review the diff, merge, and sync local `main`

This keeps `main` in a stable, working state throughout development.

## Roadmap

Beyond the initial four-week build, planned additions include:

- M-Pesa payment integration
- WhatsApp or SMS delivery notifications
- Bottle deposit tracking
- Expense and profit/loss reporting
- A REST API for potential mobile access
- Docker-based deployment

## Author

Felicia Omollo