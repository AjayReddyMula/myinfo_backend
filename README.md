# MyInfo Backend

A Django REST Framework (DRF) backend that integrates with MyInfo v4 APIs for SingPass authentication and personal data retrieval.

## 🚀 Setup

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Set Up Environment Variables
Create a `.env` file:
```ini
SECRET_KEY=your_secret_key
DEBUG=True
MYINFO_CLIENT_ID=your_client_id
MYINFO_DOMAIN=your_myinfo_domain
MYINFO_JWKS_TOKEN_VERIFICATION_URL=your_verification_url
MYINFO_JWKS_DATA_VERIFICATION_URL=your_jws_verification_url
MYINFO_PURPOSE_ID=your_value
MYINFO_PRIVATE_KEY_SIG=your_SIG_key
MYINFO_PRIVATE_KEY_ENC=your_ENC_key
REDIS_URL=redis://127.0.0.1:6379/1
```

### 3️⃣ Run Migrations & Start Server
```bash
python manage.py migrate
python manage.py runserver
```

## 🔥 Redis Cache Setup
Install and run Redis:
```bash
sudo apt install redis-server  # Linux
brew install redis  # macOS
redis-server
```

## 📌 API Endpoints

### ➤ Get Authorization URL
`GET /api/v1/myinfo/authorize/`
```json
{
  "authorize_url": "https://test.singpass.gov.sg/...",
  "state": "random_string"
}
```

### ➤ Handle Authorization Callback
`GET /api/v1/myinfo/callback/?code=&state=`

## ✅ Running Tests
```bash
python manage.py test
```
