"""Models for News app."""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
    
    
class User(db.Model):
    """User."""

    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    
    # Define relationship with UserNews
    saved_news = db.relationship('UserNews', backref='user', cascade='all, delete-orphan')
    
    @classmethod
    def register(cls, username, pwd):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(pwd)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/username and hashed pwd
        return cls(username=username, password=hashed_utf8)
    
    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            # return user instance
            return u
        else:
            return False

    
    
class News(db.Model):
    """News."""

    __tablename__ = 'news'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author = db.Column(db.String(500), nullable=True)
    title = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text, nullable=True)
    url = db.Column(db.Text, nullable=True)
    url_to_image = db.Column(db.Text, nullable=True)
    published_at = db.Column(db.DateTime, nullable=True)
    
    # Define relationship with UserNews
    saved_by_users = db.relationship('UserNews', backref='news', cascade='all, delete-orphan')
    
    
    
class UserNews(db.Model):
    """Mapping of a news to a user."""

    __tablename__ = 'user_news'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    news_id = db.Column(db.Integer, db.ForeignKey('news.id'), primary_key=True)
    
    # user = db.relationship('User', backref=db.backref('user_news', cascade='all, delete-orphan'))
    # news = db.relationship('News', backref=db.backref('user_news', cascade='all, delete-orphan'))