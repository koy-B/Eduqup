# EduTutor AI (Django MVP)

Scalable MVP backend for a tutoring platform with:
- Email/password registration and JWT login
- AI chat sessions
- Course material upload and analysis
- Quiz generation from uploaded content
- Free vs Pro feature boundaries
- Voice API placeholders for future Pro rollout

## Tech Stack
- Python 3.12 (target)
- Django 5+
- Django REST Framework
- JWT (`djangorestframework-simplejwt`)
- Django Channels (WebSocket realtime chat)
- SQLite only
- OpenAI API

## Project Structure
```
edututor_ai/
accounts/
chat/
documents/
subscriptions/
ai_services/
```

## Setup
1. Create and activate a virtual environment (Python 3.12 recommended).
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Copy env file:
```bash
cp .env.example .env
```
4. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```
5. Create admin user (optional):
```bash
python manage.py createsuperuser
```
6. Start server:
```bash
python manage.py runserver
```

## Security and Limits
- JWT-protected endpoints
- File type validation: `pdf`, `docx`, `jpg`, `jpeg`, `png`
- File size limit via `MAX_UPLOAD_SIZE_MB`
- Free-tier daily message cap via `FREE_DAILY_MESSAGE_LIMIT`
- Pro-only middleware restriction for `/api/subscriptions/voice/*`

## API Routes

### Accounts
- `POST /api/accounts/register/`
- `POST /api/accounts/login/`
- `POST /api/accounts/token/refresh/`
- `GET /api/accounts/me/`

### Chat
- `GET /api/chat/sessions/`
- `POST /api/chat/sessions/create/`
- `POST /api/chat/sessions/{session_id}/messages/`

### Web App AJAX (Session Auth)
- `GET /app/api/chat/sessions/`
- `POST /app/api/chat/sessions/create/`
- `GET /app/api/chat/sessions/{session_id}/messages/?page=1&page_size=20`
- `POST /app/api/chat/sessions/{session_id}/send/`
- `POST /app/api/documents/upload/`

### Documents
- `POST /api/documents/upload/`

### Subscriptions / Voice
- `GET /api/subscriptions/status/`
- `POST /api/subscriptions/voice/speech-to-text/` (placeholder)
- `POST /api/subscriptions/voice/text-to-speech/` (placeholder)

### WebSocket
- `WS /ws/chat/{session_id}/`
- Events:
  - client -> server: `{"type":"message","content":"..."}`
  - client -> server: `{"type":"typing","is_typing":true|false}`
  - server -> client: `{"type":"message","message":{...}}`
  - server -> client: `{"type":"typing","is_typing":true|false,"user_id":0}`

## Notes
- SQLite is explicitly configured in `edututor_ai/settings.py`.
- OpenAI integration is centralized in `ai_services/openai_service.py`.
- Document text extraction currently uses a placeholder function to keep the MVP modular and easy to extend with PDF/DOCX/OCR pipelines.
