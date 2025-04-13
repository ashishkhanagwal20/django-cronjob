# Newsletter Subscription System

A Django-React application that allows users to subscribe to topics and receive automated email newsletters with the latest news from NewsAPI.

## Features

- 🔐 JWT Authentication
- 📧 Automated Newsletter Delivery
- 📰 Real News Content via NewsAPI
- 📊 Email History Tracking
- 🎯 Topic-based Subscriptions
- ⚡ Asynchronous Task Processing

## Tech Stack

### Backend

- Django & Django REST Framework
- PostgreSQL Database
- Celery for Task Queue
- RabbitMQ as Message Broker
- JWT for Authentication
- NewsAPI for Content

### Frontend (Upcoming)

- React with Vite
- Tailwind CSS
- React Router
- Axios for API calls

## Project Setup

### Prerequisites

- Python 3.8+
- PostgreSQL
- RabbitMQ
- Node.js (for frontend)

### Installation

1. **Clone the repository**

```bash
git clone <repository-url>
cd django-project
```

2. **Set up virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Database Setup**

```bash
# In PostgreSQL
CREATE DATABASE news_db;

# In Django
python manage.py migrate
python manage.py createsuperuser
```

4. **Configuration**
   Update `backend/settings.py` with your credentials:

```python
# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'news_db',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Email
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'

# NewsAPI
NEWS_API_KEY = 'your-api-key'
```

## Running the Project

1. **Start Services**

```bash
# Terminal 1: Django Server
python manage.py runserver

# Terminal 2: Celery Worker
celery -A backend worker --pool=solo -l INFO
```

2. **Access Points**

- Django Admin: http://localhost:8000/admin
- API Root: http://localhost:8000/api/

## API Endpoints

### Authentication

- POST `/api/register/` - User registration
- POST `/api/token/` - Login (get JWT)
- POST `/api/token/refresh/` - Refresh token
- GET `/api/profile/` - User profile

### Topics

- GET `/api/topics/` - List topics
- POST `/api/topics/` - Create topic (admin)

### Subscriptions

- GET `/api/subscriptions/` - User's subscriptions
- POST `/api/subscriptions/` - Subscribe to topic
- DELETE `/api/subscriptions/{id}/` - Unsubscribe

### Emails

- GET `/api/emails/` - Email history

## Data Models

### Topic

```python
- title (CharField)
- description (TextField)
- search_query (CharField, optional)
- created_at (DateTimeField)
```

### Subscription

```python
- user (ForeignKey)
- topic (ForeignKey)
- created_at (DateTimeField)
```

### EmailHistory

```python
- user (ForeignKey)
- subject (CharField)
- content (TextField)
- sent_at (DateTimeField)
```

## Development Roadmap

### Phase 1: Backend ✅

- [x] Project Setup
- [x] Database Models
- [x] API Endpoints
- [x] JWT Authentication
- [x] Email Integration
- [x] NewsAPI Integration
- [x] Celery Tasks

### Phase 2: Frontend 🚧

- [ ] React Setup with Vite
- [ ] Authentication Flow
- [ ] Dashboard Layout
- [ ] Topic Management
- [ ] Subscription Management
- [ ] Email History Display

### Phase 3: Enhancements 📋

- [ ] Custom Email Templates
- [ ] User Preferences
- [ ] Analytics Dashboard
- [ ] Rich Text Content
- [ ] Advanced Search Filters

## Testing

### API Testing

A Postman collection is available with:

- Environment variables
- Automatic token handling
- All API endpoints
- Request/response examples

Import the collection from:

- `Newsletter_API.postman_collection.json`
- `Newsletter_API.postman_environment.json`

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.
