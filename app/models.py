from datetime import datetime, timezone
from sqlalchemy import Boolean, Float, Integer
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    posts: so.WriteOnlyMapped['Post'] = so.relationship(
        back_populates='author')

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(140))
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                               index=True)

    author: so.Mapped[User] = so.relationship(back_populates='posts')

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class Games(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    bgg_listing_id: so.Mapped[int] = so.mapped_column(Integer, nullable=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(140))
    active: so.Mapped[bool] = so.mapped_column(Boolean, default=True)
    condition: so.Mapped[str] = so.mapped_column(sa.String(140))
    pounds: so.Mapped[float] = so.mapped_column(Float, default=0.0)
    ounces: so.Mapped[float] = so.mapped_column(Float, default=0.0)
    length: so.Mapped[float] = so.mapped_column(Float, default=0.0)
    width: so.Mapped[float] = so.mapped_column(Float, default=0.0)
    height: so.Mapped[float] = so.mapped_column(Float, default=0.0) 

    def __repr__(self):
        return '<Game {}>'.format(self.body)
     
@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))