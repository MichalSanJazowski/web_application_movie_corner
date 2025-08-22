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
- Docker & Docker Compose

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
requirements.txt       # Dependencies
Dockerfile             # Docker build instructions
docker-compose.yml     # Docker Compose configuration
.dockerignore          # Ignored files for Docker
.env                   # Environment variables
```

---

## ⚙️ Running with Docker

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/movie-corner.git
   cd movie-corner
   ```

2. Create a `.env` file in the root directory with your configuration:
   ```
   APP_CONFIG_KEY=your_secret_key
   DATABASE_URL=sqlite:///movies_base.db
   TMDB_BEARER=Bearer your_tmdb_token
   MY_EMAIL=your_email
   PASSWORD=your_email_password
   ```

3. Build and run the container:
   ```bash
   docker compose up --build
   ```

4. Open the app in your browser:  
   👉 http://localhost:5002/

5. To stop the app:
   ```bash
   docker compose down
   ```

---

## 🧪 Running Tests (locally, not in Docker)
To run tests with pytest:
```bash
pytest
```

---

## 📌 Notes
- You need a **TMDB API Bearer Token** to fetch movies and TV shows.
- By default, the app uses SQLite (with persistence through Docker volume). You can configure another database in `.env`.
- Email sending (contact form) works with Gmail SMTP by default.

---

## ✨ Author
Developed by **Michal San Jazowski**
