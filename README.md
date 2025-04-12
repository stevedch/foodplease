# 🛒 FoodPlease – Django Restaurant Ordering System

A modern full-stack Django application that simulates a customer-facing online food ordering system with session-based cart, real-time quantity management, and a polished UI using MaterializeCSS.

---

## ✅ Features

- 🍔 Display a dynamic restaurant menu from a database.
- ➕ Add items to cart with automatic quantity aggregation.
- 🔢 Show item quantity and subtotal in the cart.
- 🧮 Real-time cart badge with total quantity.
- 🗑 Remove one unit or clear all of an item.
- 🧹 Clear entire cart.
- 🗂 Fixture loading for menu items.
- 🖼 Responsive design and feedback via MaterializeCSS.

---

## 🗂 Project Structure

```
foodplease/
├── core/                     # Django app logic
│   ├── fixtures/             # Initial data fixtures
│   │   └── menu_items.json
│   ├── migrations/           # Database migrations
│   ├── static/               # Static assets (images/icons)
│   │   └── img/
│   ├── templates/core/       # HTML templates
│   │   ├── cart_view.html
│   │   ├── menu_view.html
│   │   ├── home_view.html
│   │   ├── order_history_view.html
│   │   └── user_profile_view.html
│   ├── admin.py
│   ├── api.py
│   ├── apps.py
│   ├── context_processors.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── foodplease/              # Project-level configuration
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── templates/               # Global templates
│   └── base.html
├── db.sqlite3               # SQLite database
├── manage.py                # Django CLI tool
└── requirements.txt         # Dependencies
```

---

## 🚀 Setup Instructions

### 1. Clone & enter project:

```bash
git clone https://github.com/stevedch/foodplease.git
cd foodplease
```

### 2. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies:

```bash
pip install -r requirements.txt
```

### 4. Apply database migrations:

```bash
python manage.py migrate
```

### 5. Load menu items from fixture:

```bash
python manage.py loaddata core/fixtures/menu_items.json
```

### 6. Run development server:

```bash
python manage.py runserver
```

Visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🧪 Admin & Fixtures

### Create a superuser:

```bash
python manage.py createsuperuser
```

### Export menu items to fixture:

```bash
python manage.py dumpdata core.MenuItem --indent 2 > core/fixtures/menu_items.json
```

---

## 🧠 Context Processor

To keep cart quantity visible in the navbar at all times, the context processor `core/context_processors.py` is registered in `settings.py`:

```python
TEMPLATES = [
    {
        ...
        'OPTIONS': {
            'context_processors': [
                ...
                'core.context_processors.cart_item_count',
            ],
        },
    },
]
```
