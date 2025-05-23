# Votely 🗳️

**Votely** is a simple and modern platform for creating and managing online polls. This project is built using **Python** and the **Django** framework, with **Django REST Framework (DRF)** for building the API.

## Features

- User registration and authentication
- Any registered user can create a poll
- Ability to set a deadline for each poll
- Polls automatically close after the deadline — no further votes allowed
- Only registered users can vote
- Fully API-based for easy integration with frontends or mobile apps

## Why the name "Votely"?

The name **Votely** is a combination of the word **"Vote"** and the suffix **"-ly"**, commonly used in modern, startup-style brand names (e.g., Bitly, Grammarly). It gives a sense of simplicity, speed, and a modern touch — and it's easy to remember.

## Technologies Used

- Python 🐍
- Django 🌐
- Django REST Framework 🔗
- SQLite (for development)
- JWT or Session Authentication (optional)

## Installation

```bash
git clone https://github.com/yourusername/votely.git
cd votely
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
