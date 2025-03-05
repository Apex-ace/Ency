# Ency - Event Management System

A comprehensive event management system built with Flask that allows organizations to create, manage, and track events while providing an easy booking interface for attendees.

## Features

- User Authentication (Students, Organizers, Admins)
- Event Creation and Management
- Individual and Group Booking
- QR Code Ticket Generation
- Payment Integration
- Review System
- Admin Dashboard
- Email Notifications
- Mobile Responsive Design

## Tech Stack

- Flask
- Supabase (PostgreSQL)
- SQLAlchemy
- Flask-Login
- QR Code Generation
- Bootstrap 5

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Apex-ace/Ency.git
cd Ency
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your configuration:
```env
FLASK_ENV=development
SECRET_KEY=your-secret-key
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_HOST=your-db-host
DB_NAME=your-db-name
DB_PORT=5432
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key
```

5. Run the application:
```bash
python moon/app.py
```

## Default Admin Credentials

- Email: admin@example.com
- Password: admin123

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 