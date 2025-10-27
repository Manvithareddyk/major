from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///social_media.db'
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Cyberbullying keywords (basic implementation)
CYBERBULLYING_KEYWORDS = [
    'hate', 'stupid', 'ugly', 'loser', 'die', 'kill', 'worthless', 'pathetic', 
    'dumb', 'idiot', 'shut up', 'go away', 'nobody likes you', 'freak', 'weirdo'
]

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_banned = db.Column(db.Boolean, default=False)
    warning_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_approved = db.Column(db.Boolean, default=True)
    sentiment_score = db.Column(db.Float)
    sentiment_label = db.Column(db.String(20))
    is_flagged = db.Column(db.Boolean, default=False)
    flagged_reason = db.Column(db.String(200))

class FlaggedAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    reason = db.Column(db.String(200), nullable=False)
    admin_reviewed = db.Column(db.Boolean, default=False)
    action_taken = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref='flags')
    post = db.relationship('Post', backref='flags')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def detect_cyberbullying(text):
    """Detect cyberbullying using keywords and sentiment analysis"""
    text_lower = text.lower()

    # Check for cyberbullying keywords
    for keyword in CYBERBULLYING_KEYWORDS:
        if keyword in text_lower:
            return True, f"Contains cyberbullying keyword: {keyword}"

    # Check sentiment
    scores = analyzer.polarity_scores(text)
    if scores['compound'] <= -0.5:  # Very negative sentiment
        return True, "Very negative sentiment detected"

    return False, "Content appears safe"

def analyze_sentiment(text):
    """Analyze sentiment of text"""
    scores = analyzer.polarity_scores(text)
    compound = scores['compound']

    if compound >= 0.05:
        return 'positive', compound
    elif compound <= -0.05:
        return 'negative', compound
    else:
        return 'neutral', compound

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated and current_user.is_banned:
        flash('Your account has been banned for violating community guidelines.', 'danger')
        logout_user()
        return redirect(url_for('login'))

    # Only show approved posts from non-banned users
    posts = Post.query.join(User).filter(
        Post.is_approved == True,
        User.is_banned == False
    ).order_by(Post.created_at.desc()).all()

    return render_template('index.html', posts=posts)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'danger')
            return redirect(url_for('register'))

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('Registration successful!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            if user.is_banned:
                flash('Your account has been banned.', 'danger')
                return redirect(url_for('login'))
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/post', methods=['POST'])
@login_required
def create_post():
    if current_user.is_banned:
        flash('You cannot post while banned.', 'danger')
        return redirect(url_for('index'))

    content = request.form['content']

    # Analyze content for cyberbullying
    is_bullying, reason = detect_cyberbullying(content)
    sentiment_label, sentiment_score = analyze_sentiment(content)

    # Create post
    post = Post(
        content=content,
        user_id=current_user.id,
        sentiment_score=sentiment_score,
        sentiment_label=sentiment_label
    )

    # If cyberbullying detected or negative sentiment
    if is_bullying or sentiment_label == 'negative':
        post.is_approved = False
        post.is_flagged = True
        post.flagged_reason = reason if is_bullying else "Negative content detected"

        # Flag the account
        flag = FlaggedAccount(
            user_id=current_user.id,
            post_id=post.id,
            reason=post.flagged_reason
        )

        # Increase warning count
        current_user.warning_count += 1

        db.session.add(post)
        db.session.commit()  # Commit to get post.id

        flag.post_id = post.id
        db.session.add(flag)
        db.session.commit()

        flash('Your post has been flagged for review by administrators.', 'warning')
    else:
        # Approve positive/neutral posts
        post.is_approved = True
        db.session.add(post)
        db.session.commit()
        flash('Post created successfully!', 'success')

    return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('index'))

    # Get flagged accounts and posts
    flagged_accounts = FlaggedAccount.query.filter_by(admin_reviewed=False).all()
    flagged_posts = Post.query.filter_by(is_flagged=True, is_approved=False).all()

    return render_template('admin.html', 
                         flagged_accounts=flagged_accounts, 
                         flagged_posts=flagged_posts)

@app.route('/admin/review/<int:flag_id>/<action>')
@login_required
def admin_review(flag_id, action):
    if not current_user.is_admin:
        flash('Access denied.', 'danger')
        return redirect(url_for('index'))

    flag = FlaggedAccount.query.get_or_404(flag_id)
    user = flag.user
    post = flag.post

    if action == 'ban':
        user.is_banned = True
        flag.action_taken = 'User banned'
        flash(f'User {user.username} has been banned.', 'success')
    elif action == 'warn':
        user.warning_count += 1
        flag.action_taken = 'Warning issued'
        flash(f'Warning issued to {user.username}.', 'success')
    elif action == 'approve':
        post.is_approved = True
        post.is_flagged = False
        flag.action_taken = 'Post approved'
        flash('Post has been approved.', 'success')
    elif action == 'reject':
        flag.action_taken = 'Post rejected'
        flash('Post has been rejected.', 'success')

    flag.admin_reviewed = True
    db.session.commit()

    return redirect(url_for('admin_dashboard'))

@app.route('/profile/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(user_id=user.id, is_approved=True).order_by(Post.created_at.desc()).all()
    return render_template('profile.html', user=user, posts=posts)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # Create admin user if doesn't exist
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin', email='admin@example.com', is_admin=True)
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("Admin user created: admin/admin123")

    app.run(debug=True)
