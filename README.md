
# Social Media Backend

This is a beginner-friendly social media backend built with Django and Django REST Framework. It includes features like user authentication, post creation, following/unfollowing, and user actions like hide/block.

## Features
- User Registration & JWT Authentication
- Post Creation & Feed
- Follow/Unfollow
- Hide/Block User Actions

## How to Run
1. Clone the repository:
   ```bash
   git clone <repository-URL>
   cd social_media_backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
4. Start the server:
   ```bash
   python manage.py runserver
   ```

## API Endpoints
- **Register**: `POST /api/auth/register/`
- **Login**: `POST /api/auth/login/`
- **Posts**: `GET /api/posts/`
- **Feed**: `GET /api/feed/`
- **Follow/Unfollow**: `POST /api/users/<username>/follow/`, `POST /api/users/<username>/unfollow/`
- **User Actions**: `POST /api/users/<username>/action/`

## License
MIT
```

You can copy and paste this as is into your `README.md` file.