import os
import pytest
from app import create_app
from app.extensions import db as _db
from app.models import User
from werkzeug.security import generate_password_hash


@pytest.fixture(scope="session")
def app():

    os.environ["APP_CONFIG_KEY"] = "test-secret"
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"
    os.environ["TMDB_BEARER"] = "Bearer TEST"
    os.environ["MY_EMAIL"] = "test@example.com"
    os.environ["PASSWORD"] = "pwd"


    app = create_app()
    app.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=False
    )


    with app.app_context():
        _db.drop_all()
        _db.create_all()
    yield app


@pytest.fixture()
def db(app):
    with app.app_context():
        yield _db
        for table in reversed(_db.metadata.sorted_tables):
            _db.session.execute(table.delete())
        _db.session.commit()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def user(db):
    u = User(
        email="user@example.com",
        name="User",
        password=generate_password_hash("pass123", method="pbkdf2:sha256", salt_length=8),
    )
    db.session.add(u)
    db.session.commit()
    return u


@pytest.fixture()
def login(client, user):
    def _login(email="user@example.com", password="pass123"):
        return client.post("/login", data={"email": email, "password": password}, follow_redirects=True)
    return _login
