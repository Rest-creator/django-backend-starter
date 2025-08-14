
# **Django Backend Starter – Clean Architecture Boilerplate**

A production-ready **Django backend starter template** that applies **Clean Architecture** principles to keep business logic **reusable**, **framework-agnostic**, and **maintainable**.

This structure helps you:

* **Speed up development** by separating reusable core logic from framework code.
* Keep your **business rules portable** — they can be reused in Django, FastAPI, Flask, or even microservices.
* Make testing and scaling much easier.


## **Why Use This Starter?**

When building backends, many developers accidentally couple **business logic** directly to the **framework** (e.g., Django models, DRF serializers).
This makes code hard to test, maintain, or reuse in other projects.

This starter **solves that problem** by:

1. Splitting code into **three layers**:

   * **Core** → Pure Python business logic (reusable anywhere).
   * **Adapters** → Implementations that connect core logic to Django ORM, auth, and APIs.
   * **Application** → Django apps, views, and serializers (presentation layer).

2. Providing **ready-made interfaces** so swapping the database or framework requires minimal changes.
3. Encouraging **testable, modular design**.


## **Folder Structure**

```
django-backend-starter/
│
├── core/                   # Pure business logic (NO Django imports)
│   ├── entities/           # Domain models (dataclasses)
│   ├── services/           # Business rules and workflows
│   ├── interfaces/         # Abstract interfaces for DB & APIs
│   └── utils/              # Shared helpers (logging, validation, etc.)
│
├── adapters/               # Django-specific implementations
│   ├── repositories/       # Django ORM repositories
│   ├── auth/               # Auth providers (JWT, OAuth, etc.)
│   └── external/           # Third-party API clients
│
├── project_name/           # Django project settings & entry points
│   ├── settings.py         # Django & environment configuration
│   ├── urls.py             # Global URL routing
│   └── wsgi.py             # WSGI application entrypoint
│
├── apps/                   # Django apps (presentation layer)
│   └── users/
│       ├── models.py       # ORM models (DB schema)
│       ├── serializers.py  # DRF serializers
│       ├── views.py        # API views
│       ├── urls.py         # App-specific routing
│       └── admin.py        # Admin site configuration
│
├── config/                 # Environment variables & settings loader
│   ├── settings.py
│   └── .env.example
│
├── tests/                  # Unit & integration tests
│
├── manage.py               # Django management commands
└── requirements.txt        # Python dependencies
```


## **What Goes Where**

### **1. `/core` – Reusable Business Logic**

* **`entities/`** → Pure data models (e.g., `User`, `Loan`, `Invoice`) using Python’s `@dataclass`.
* **`services/`** → Business rules (e.g., registration, payment processing, loan calculation).
* **`interfaces/`** → Abstract contracts for persistence, APIs, and auth — implemented in `/adapters`.
* **`utils/`** → Cross-cutting helpers like logging, validators, formatters.

**Tip:** `/core` has no Django imports — you can copy this folder into another project without changes.

---

### **2. `/adapters` – Framework Implementations**

* **`repositories/`** → Concrete implementations of `core/interfaces`, using Django ORM.
* **`auth/`** → Adapters for authentication/authorization.
* **`external/`** → Integrations with third-party APIs (payment gateways, messaging services).

**Tip:** If you swap Django ORM for SQLAlchemy or another DB, you only touch `/adapters`.

---

### **3. `/apps` – Django Presentation Layer**

* Contains Django apps with **views**, **serializers**, and **URL routing**.
* Talks to **`core/services`** through dependency injection.
* Handles HTTP requests/responses but delegates business rules to `/core`.

---

### **4. `/config` – Environment & Settings**

* Centralized configuration (via `.env`) so you can easily change DB URLs, API keys, etc., without touching code.

---

## **Getting Started**

### **1. Clone the Repo**

```bash
git clone https://github.com/Rest-creator/django-backend-starter.git
cd django-backend-starter
```

### **2. Install Dependencies**

```bash
pip install -r requirements.txt
```

### **3. Set Up Environment Variables**

```bash
cp config/.env.example .env
```

Edit `.env` with your values.

### **4. Run Migrations**

```bash
python manage.py migrate
```

### **5. Start Development Server**

```bash
python manage.py runserver
```

---

## **Example: Adding a New Feature**

Say you want to add **"Register User"** functionality:

1. **Core Layer (`/core/services/user_service.py`)**

   * Write business logic for creating users.
2. **Core Interface (`/core/interfaces/user_repository.py`)**

   * Define how the service will save users.
3. **Adapter (`/adapters/repositories/user_repository_django.py`)**

   * Implement saving users with Django ORM.
4. **App Layer (`/apps/users/views.py`)**

   * Create a DRF API view that calls the service.

Result:

* Your registration logic is in `/core` and can be reused in any other backend.
* Django just handles **how** it’s connected to a database and exposed via API.

---

## **Benefits**

✅ **Reusable** — `/core` can be used in any Python backend.
✅ **Testable** — Mock interfaces for unit testing without DB/API calls.
✅ **Maintainable** — Changes in business rules don’t break the framework layer.
✅ **Scalable** — Easy to swap databases, frameworks, or API integrations.


