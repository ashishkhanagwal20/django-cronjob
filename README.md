# Newsletter Subscription System

A full-stack application for managing newsletter subscriptions and automated email delivery using Django, Celery, and React.

## Features

- 🔐 JWT Authentication
- 📧 Automated Newsletter Delivery
- 📱 Responsive Dashboard
- 📊 Email History Tracking
- 🎯 Topic-based Subscriptions
- ⏰ Scheduled Newsletter Delivery
- 🌐 REST API
- 📝 Rich Text Newsletter Content

## Tech Stack

### Backend

- Django
- Django REST Framework
- PostgreSQL
- Celery
- Redis
- JWT Authentication

### Frontend

- React (Vite)
- Tailwind CSS
- Axios
- React Router
- Context API

## Prerequisites

- Python 3.8+
- Node.js 16+
- PostgreSQL
- Redis
- RabbitMQ

## Setup Instructions

### Backend Setup

1. Create and activate virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create `.env` file in the root directory with the following variables:

   ```env
   # Django Settings
   SECRET_KEY=your_secret_key
   DEBUG=True

   # Database
   DB_NAME=your_db_name
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=localhost
   DB_PORT=5432

   # Email Settings
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your_email
   EMAIL_HOST_PASSWORD=your_app_password

   # NewsAPI
   NEWS_API_KEY=your_api_key

   # Celery
   CELERY_BROKER_URL=amqp://guest:guest@localhost:5672//
   ```

4. Run migrations:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Create superuser:

   ```bash
   python manage.py createsuperuser
   ```

6. Start Celery worker:

   ```bash
   celery -A backend worker -l info
   ```

7. Start Celery beat:

   ```bash
   celery -A backend beat -l info
   ```

8. Run the development server:
   ```bash
   python manage.py runserver
   ```

### Frontend Setup (Coming Soon)

1. Navigate to frontend directory:

   ```bash
   cd frontend
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Start development server:
   ```bash
   npm run dev
   ```

## API Documentation

### Authentication Endpoints

- POST `/api/token/` - Obtain JWT token pair
- POST `/api/token/refresh/` - Refresh JWT token
- POST `/api/register/` - Register new user

### Topic Endpoints

- GET `/api/topics/` - List all topics
- POST `/api/topics/` - Create new topic (Admin only)
- GET `/api/topics/{id}/` - Retrieve topic details
- PUT `/api/topics/{id}/` - Update topic (Admin only)
- DELETE `/api/topics/{id}/` - Delete topic (Admin only)

### Subscription Endpoints

- GET `/api/subscriptions/` - List user's subscriptions
- POST `/api/subscribe/` - Subscribe to a topic
- DELETE `/api/subscribe/{id}/` - Unsubscribe from topic

### Email History Endpoints

- GET `/api/emails/` - List email history
- GET `/api/emails/{id}/` - Get specific email details

## Testing

### Backend Tests

Run the test suite:

```bash
python manage.py test
```

### API Testing with Postman

A Postman collection is available with:

- Environment variables
- Automatic token handling
- All API endpoints configured
- Request/response examples

Import the collection from `postman/Newsletter_API.postman_collection.json`

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
