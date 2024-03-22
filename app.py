from flask import Flask, redirect, render_template, request, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
import os
import requests
from models import db, connect_db, User, News, UserNews
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'postgresql:///news-app')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

API_KEY_FOR_NEWS = '176d68e99ae645d58ccda406bd557916'

connect_db(app)
app.app_context().push()
# db.create_all()

app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"
bcrypt = Bcrypt(app)
debug = DebugToolbarExtension(app)


@app.route("/")
def root():
    """Homepage: redirect to /login."""
    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():
    """User registration."""
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template("register.html", error="Username already exists")

        hashed_pwd = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(username=username, password=hashed_pwd)
        db.session.add(new_user)
        db.session.commit()

        session['user_id'] = new_user.id  # Set session for logged-in user
        return redirect("/dashboard")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """User login."""
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id  # Set session for logged-in user
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    """User dashboard."""
    user_id = session.get('user_id')

    if user_id:
        user = User.query.get(user_id)

        # Fetch news from NewsAPI
        response = requests.get('https://newsapi.org/v2/top-headlines',
                                params={'apiKey': API_KEY_FOR_NEWS, 'country': 'us'})
        articles = response.json()

        return render_template("dashboard.html", user=user, articles=articles)
    else:
        return redirect("/login")
    
@app.route("/news")
def get_news():
    """Get filtered news articles from NewsAPI."""
    search_query = request.args.get('q', '')  # Default search query: empty string
    category = request.args.get('category', '')  # Optional category filter
    country = request.args.get('country', 'us')  # Default country: United States

    params = {'apiKey': API_KEY_FOR_NEWS, 'country': country}
    if search_query:
        params['q'] = search_query
    if category:
        params['category'] = category

    response = requests.get('https://newsapi.org/v2/top-headlines', params=params)

    articles = response.json()['articles'] if response.status_code == 200 else []

    return jsonify({'articles': articles})

@app.route("/save-news", methods=["POST"])
def save_news():
    """Save news article to the database."""
    author = request.json.get('author')
    title = request.json.get('title')
    description = request.json.get('description')
    url = request.json.get('url')
    url_to_image = request.json.get('url_to_image')
    published_at = request.json.get('published_at')

    new_article = News(author=author, title=title, description=description,
                        url=url, url_to_image=url_to_image, published_at=published_at)
    
    db.session.add(new_article)
    db.session.commit()

    # Associate the saved news with the current user
    user_id = session.get('user_id')
    if user_id:
        user_news = UserNews(user_id=user_id, news_id=new_article.id)
        db.session.add(user_news)
        db.session.commit()
    else:
        return jsonify(message="User not logged in"), 401  # Unauthorized

    return jsonify(message="News saved successfully"), 201  # Status code 201: Created

@app.route("/saved-news")
def saved_news():
    """Display saved news articles for the logged-in user."""
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        saved_articles = (
                            db.session.query(News)
                            .join(UserNews)
                            .filter(UserNews.user_id == user_id)
                            .order_by(UserNews.news_id.desc())  # Order by news_id in descending order
                            .all()
                        )
        return render_template("saved-news.html", user=user, saved_articles=saved_articles)
    else:
        return redirect("/login")
    
@app.route("/unsave-news", methods=["POST"])
def unsave_news():
    """Remove saved news article for the logged-in user."""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify(message="User not logged in"), 401  # Unauthorized

    news_id = request.json.get('news_id')
    user_news = UserNews.query.filter_by(user_id=user_id, news_id=news_id).first()
    if user_news:
        db.session.delete(user_news)
        db.session.commit()
        return jsonify(message="News unsaved successfully"), 200
    else:
        return jsonify(message="News not found for user"), 404

    
@app.route("/logout", methods=["POST"])
def logout():
    """User logout."""
    session.pop('user_id', None)
    return redirect("/login")
