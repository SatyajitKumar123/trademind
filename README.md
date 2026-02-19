# TradeMind

**TradeMind** is a backend system for analyzing trading performance from broker tradebooks.
It ingests CSV exports (e.g., Zerodha), reconstructs executions using a **FIFO matching engine**, and provides **portfolio analytics APIs** such as P&L, equity curve, and risk metrics.

Built to demonstrate **production-style backend architecture** using Django, DRF, async processing, and containerization.

---

## 🚀 Features

* 📥 **Broker CSV Ingestion**

  * Adapter-based parsing (broker-agnostic design)
  * Normalizes trade data into domain DTOs

* 🧠 **FIFO Matching Engine**

  * Matches BUY ↔ SELL trades deterministically
  * Generates realized P&L records

* 🔁 **Idempotent Uploads**

  * File hashing prevents duplicate ingestion
  * Ensures consistent analytics (no accidental reprocessing)

* ⚙️ **Asynchronous Processing**

  * Large tradebooks processed via **Celery + Redis**
  * Upload returns immediately while background job runs

* 🔐 **User-Scoped Data**

  * JWT authentication
  * Each user sees only their trades and analytics

* 📊 **Analytics APIs**

  * Dashboard summary (win rate, expectancy, net P&L)
  * Equity curve generation
  * Risk metrics (drawdown, profit factor, R:R)

* 🐳 **Dockerized Environment**

  * Reproducible setup with Postgres, Redis, Worker

---

## 🏗️ Tech Stack

| Layer            | Technology                     |
| ---------------- | ------------------------------ |
| Backend          | Django + Django REST Framework |
| Database         | PostgreSQL                     |
| Async Jobs       | Celery + Redis                 |
| Auth             | JWT (SimpleJWT)                |
| Containerization | Docker Compose                 |
| Testing          | Pytest + Django Test Suite     |

---

## 📐 Architecture Overview

TradeMind follows a **service-layer architecture** to keep business logic independent of Django views.

```
API Layer (DRF)
   ↓
Service Layer (Pure business logic)
   ↓
Domain Layer (FIFO engine, DTOs)
   ↓
Persistence Layer (Django ORM)
```

This separation allows:

* Easier testing
* Reusable logic between UI and APIs
* Cleaner scaling into microservices later

---

## 🔄 Trade Ingestion Flow

```
Upload CSV
   ↓
Compute File Hash (duplicate protection)
   ↓
Create UploadJob (PENDING)
   ↓
Celery Worker Processes File
   ↓
FIFO Matching Engine
   ↓
Persist Trades + Realized PnL (atomic transaction)
   ↓
Update Job Status → DONE
```

Atomic transactions ensure **no partial data is saved** if processing fails.

---

## 🔐 Authentication

TradeMind uses **JWT authentication**.

### Get Token

```http
POST /api/jwt/token/
```

Body:

```json
{
  "username": "your_user",
  "password": "your_password"
}
```

Response:

```json
{
  "access": "...",
  "refresh": "..."
}
```

Use token in headers:

```
Authorization: Bearer <access_token>
```

---

## 📊 Example API Endpoints

| Endpoint                              | Description         |
| ------------------------------------- | ------------------- |
| POST `/api/v1/trades/upload/`         | Upload tradebook    |
| GET `/api/v1/dashboard/summary/`      | Performance summary |
| GET `/api/v1/dashboard/equity-curve/` | Equity curve        |
| GET `/api/v1/dashboard/risk-metrics/` | Risk analysis       |
| GET `/api/v1/trades/upload/<job_id>/` | Upload job status   |

---

## 🐳 Running With Docker (Recommended)

### 1️⃣ Create environment file

Create `.env.docker`:

```
POSTGRES_DB=trademind
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DJANGO_SECRET_KEY=dev-secret
```

### 2️⃣ Build and start services

```bash
docker compose up --build
```

### 3️⃣ Run migrations

```bash
docker compose exec web python manage.py migrate
```

### 4️⃣ Create superuser

```bash
docker compose exec web python manage.py createsuperuser
```

---

## 💻 Running Locally (Without Docker)

Install dependencies:

```bash
pip install -r requirements.txt
```

Start Postgres & Redis, then:

```bash
python manage.py migrate
python manage.py runserver
celery -A config worker -l info
```

---

## 🧪 Running Tests

```bash
pytest
```

Tests cover:

* FIFO matching correctness
* Upload deduplication
* Analytics calculations
* API authentication flows

---

## 📊 Key Design Decisions

### Why FIFO Matching?

Markets settle positions FIFO; accurate realized P&L requires deterministic lot matching.

### Why Background Jobs?

Tradebooks can contain thousands of rows — async processing prevents API blocking.

### Why File Hashing Instead of Filename Check?

Broker exports may reuse filenames. Hashing ensures validation based on **content**, not metadata.

### Why Service Layer?

Prevents “fat views / fat models” and keeps domain logic testable.

---

## 📌 Future Improvements

* Broker adapters for more platforms
* Real-time trade ingestion
* Strategy tagging & journaling
* WebSocket progress tracking
* Portfolio-level analytics

---

## 👤 Author

**Satyajit Kumar**
Backend Developer (Python/Django)

Focused on building reliable, production-style backend systems with clear architecture and data integrity.
