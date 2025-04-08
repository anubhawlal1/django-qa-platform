# Q&A Platform

A Django-based Question & Answer platform similar to Stack Overflow or Quora where users can ask questions, provide answers, and interact with the community.

## Features

### User Authentication
- User registration with email verification
- Custom password validation:
  - Minimum 8 characters
  - At least one letter
  - At least one capital letter
  - At least one number
  - At least one special character
  - Password cannot be similar to username
- Real-time password strength indicator
- Password confirmation with match indicator
- Login/Logout functionality
- Protected routes for authenticated users

### Questions
- View all questions on the home page
- Questions display:
  - Title
  - Content preview (truncated to 50 words)
  - Author name
  - Creation timestamp
  - Number of answers
- Create new questions (authenticated users only)
- Detailed question view with full content

### Answers
- Post answers to questions (authenticated users only)
- View all answers for a question
- Answers display:
  - Full content
  - Author name
  - Creation timestamp
  - Like count
- Like/Unlike answers (authenticated users only)

### User Interface
- Clean, modern Bootstrap-based design
- Responsive layout for all screen sizes
- Font Awesome icons for visual feedback
- Real-time form validation feedback
- Success/Error message notifications
- Intuitive navigation

### Security Features
- CSRF protection
- Password hashing
- Cache control headers
- Form validation
- Protected API endpoints
- Secure session handling

## Project Structure
```
qflow/
├── manage.py
├── qflow/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── qa/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── urls.py
├── templates/
│   ├── base.html
│   ├── qa/
│   │   ├── home.html
│   │   ├── question_detail.html
│   │   └── question_form.html
│   └── registration/
│       ├── login.html
│       ├── register.html
│       └── logged_out.html
└── static/
    └── css/
        └── styles.css
```

## Models
- **User** (Django's built-in User model)
- **Question**
  - title
  - content
  - author (ForeignKey to User)
  - created_at
- **Answer**
  - content
  - author (ForeignKey to User)
  - question (ForeignKey to Question)
  - created_at
  - likes (ManyToManyField with User)

## URL Patterns
- Home: `/`
- Register: `/register/`
- Login: `/accounts/login/`
- Logout: `/logout/`
- Create Question: `/question/new/`
- Question Detail: `/question/<int:pk>/`
- Like Answer: `/answer/<int:pk>/like/`

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/yourusername/qflow.git
cd qflow
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply migrations:
```bash
python manage.py migrate
```

5. Create superuser (optional):
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

7. Visit http://127.0.0.1:8000 in your browser

## Usage Guidelines

### Asking Questions
1. Click "Want to ask a question?" (redirects to login if not authenticated)
2. Log in or register if needed
3. Fill in the question title and content
4. Submit the question

### Answering Questions
1. Navigate to a question
2. Scroll to the answer form at the bottom
3. Write your answer
4. Submit (requires authentication)

### Liking Answers
1. View any question with answers
2. Click the thumbs-up icon on any answer
3. The like count will update instantly

## Security Considerations
- All passwords are hashed using Django's password hashers
- CSRF protection is enabled for all POST requests
- Cache control headers prevent sensitive data caching
- Form validation occurs both client-side and server-side
- Authentication required for sensitive operations
- SQL injection protection via Django's ORM
- XSS protection via Django's template system

## Browser Compatibility
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Responsive design works on mobile devices

## Known Issues
- Cache control headers may need adjustment for production
- Password reset functionality not implemented yet
- No email verification system in place
- No pagination for questions/answers lists

## Future Enhancements
- Email verification for new accounts
- Password reset functionality
- Question categories/tags
- User profiles
- Search functionality
- Rich text editor for questions/answers
- Answer acceptance feature
- Question voting system
- Comment system
- User reputation system
- API endpoints for mobile apps