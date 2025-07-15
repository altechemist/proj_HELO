# HELO Project

This is a Django-based web application for managing healthcare logistics, including user accounts, medication management, ride scheduling, support, and tracking.

## Features

- User authentication and account management
- Admin portal for staff
- Dashboard for users
- Medication management
- Ride scheduling and management
- Support ticketing system
- Real-time tracking

## Project Structure

- `HELO/` - Main Django project settings
- `accounts/` - User account management
- `admin_portal/` - Admin-specific features
- `dashboard/` - User dashboard
- `medications/` - Medication management
- `rides/` - Ride scheduling and management
- `support/` - Support ticketing
- `tracking/` - Real-time tracking
- `templates/` - Shared HTML templates
- `static/` - Static files (CSS, JS, images)

## Setup Instructions

1. **Clone the repository**
2. **Create and activate a virtual environment** (if not already):

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies:**

   ```powershell
   pip install -r requirements.txt
   ```

4. **Apply migrations:**

   ```powershell
   python manage.py migrate
   ```

5. **Run the development server:**

   ```powershell
   python manage.py runserver
   ```

## Requirements

See `requirements.txt` for Python package dependencies.

## License

[MIT License](LICENSE)