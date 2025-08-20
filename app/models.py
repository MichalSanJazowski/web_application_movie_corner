from sqlalchemy import UniqueConstraint, ForeignKey, Integer, String, Text
from sqlalchemy.orm import mapped_column, Mapped, relationship
from flask_login import UserMixin
from .extensions import db

class Movies(db.Model):
    __tablename__ = "movies"
    __table_args__ = (UniqueConstraint("user_id", "title", name="uq_user_movie_title"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    year: Mapped[int | None]
    description: Mapped[str | None] = mapped_column(Text)
    rating: Mapped[float | None]
    ranking: Mapped[int | None]
    review: Mapped[str | None] = mapped_column(Text)
    img_url: Mapped[str | None] = mapped_column(String(250))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="movies")

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(100))
    role: Mapped[str] = mapped_column(String(20), default="user")
    movies = relationship("Movies", back_populates="owner", cascade="all, delete-orphan")
