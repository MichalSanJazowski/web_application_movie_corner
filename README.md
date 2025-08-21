# 🎬 Movie Corner - Flask Web Application

Movie Corner is a simple web application built with **Flask**.  
It allows users to register, log in, browse movies and TV shows (via the TMDB API), and manage their own movie ranking list.

---

## 🚀 Features
- User authentication (signup, login, logout)
- Add movies to your personal ranking
- Edit movie rating and review
- Delete movies from your list
- Browse latest movies and TV shows (fetched from [The Movie Database API](https://www.themoviedb.org/))
- News section (scraped from ScreenRant)
- Contact form with email sending
- Admin-only routes protection
- Basic tests with **pytest**

---

## 🛠️ Tech Stack
- Python 3.12
- Flask (with Blueprints)
- SQLAlchemy
- Flask-Login
- Flask-WTF
- Bootstrap 5
- Flask-CKEditor
- Flask-Session
- Pytest (for testing)

---

## 📂 Project Structure
```
app/
 ├── blueprints/       # auth, main, movies modules
 ├── templates/        # HTML templates
 ├── static/           # CSS, JS, images
 ├── models.py         # Database models
 ├── forms.py          # WTForms classes
 ├── config.py         # App configuration
 ├── extensions.py     # Extensions initialization
 └── __init__.py       # create_app factory

tests/                 # pytest tests
run.py                 # Entry point
requirements.txt       # Dependencies
Procfile               # For deployment
```

---

## ⚙️ Installation & Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/movie-corner.git
   cd movie-corner
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # on Linux/Mac
   venv\Scripts\activate      # on Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory with:
   ```
   APP_CONFIG_KEY=your_secret_key
   DATABASE_URL=sqlite:///movies_base.db
   TMDB_BEARER=Bearer your_tmdb_token
   MY_EMAIL=your_email
   PASSWORD=your_email_password
   ```

5. Run the application:
   ```bash
   python run.py
   ```
   The app will be available at:  
   👉 http://127.0.0.1:5002/

---

## 🧪 Running Tests
To run tests with pytest:
```bash
pytest
```

---

## 📌 Notes
- You need a **TMDB API Bearer Token** to fetch movies and TV shows.
- The app uses SQLite by default, but you can configure another database in `.env`.
- Email sending (contact form) works with Gmail SMTP by default.

---

## ✨ Author
Developed by **Michal San Jazowski**
