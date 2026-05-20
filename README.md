# PropertyBazaar - Real Estate Platform

A complete, production-ready Real Estate Property Buy/Sell website built with Python, Django, and modern web technologies.

## Features

- **Authentication**: Custom User model, Email OTP, Social Login (Allauth).
- **Properties**: CRUD for listings, Categories, Amenities, Multi-image/video support.
- **Search & Filters**: Advanced search by location, price, type, etc.
- **Interactions**: Wishlist, Property Comparison, Site Visit Scheduling.
- **Communication**: Contact owner via inquiry forms, In-app notifications.
- **Payments**: Razorpay integration for featured listings.
- **Blog**: SEO-friendly articles with CKEditor support.
- **Dashboard**: Role-based dashboards for Buyers, Sellers, and Agents.
- **Modern UI**: Built with Bootstrap 5 and premium custom CSS.

## Tech Stack

- **Backend**: Django 5+, Django REST Framework
- **Database**: PostgreSQL (Dockerized)
- **Frontend**: Bootstrap 5, Vanilla JS, AJAX
- **Containerization**: Docker, Docker Compose
- **Payments**: Razorpay

## Getting Started

### Prerequisites

- Python 3.12+
- Docker & Docker Compose (Optional but recommended)

### Local Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd PropertyBazaar_Pytn
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file from the template provided.

5. **Run Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Start Development Server**:
   ```bash
   python manage.py runserver
   ```

### Using Docker

```bash
docker-compose up --build
```

## Admin Access

Create a superuser to access the Django admin panel:
```bash
python manage.py createsuperuser
```
Access at: `http://localhost:8000/admin/`

## License

This project is licensed under the MIT License.
