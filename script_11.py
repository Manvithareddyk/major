# Create README.md with installation and usage instructions
readme_content = '''# SafeSpace - Social Media Platform with Cyberbullying Detection

A modern social media platform that uses AI to detect and prevent cyberbullying, ensuring only positive and neutral content is shared.

## Features

- **AI-Powered Cyberbullying Detection**: Automatic detection of negative content using sentiment analysis and keyword filtering
- **Real-time Content Filtering**: Only positive and neutral comments are allowed to be posted
- **Admin Panel**: Comprehensive dashboard for reviewing flagged accounts and content
- **User Management**: Account warnings, bans, and user statistics
- **Responsive Design**: Mobile-friendly interface built with Bootstrap
- **Real-time Notifications**: Instant alerts for flagged content

## Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite (easily replaceable with PostgreSQL/MySQL)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **AI/ML**: VADER Sentiment Analysis, Custom keyword filtering
- **Authentication**: Flask-Login

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Steps

1. **Clone or download the project**
   ```bash
   cd social_media_cyberbullying_detector
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize NLTK data** (for sentiment analysis)
   ```python
   python -c "import nltk; nltk.download('vader_lexicon')"
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   - Open your web browser and go to `http://localhost:5000`
   - The app will automatically create the database and admin user

## Default Admin Account

- **Username**: admin
- **Password**: admin123

Use this account to access the admin panel at `/admin`

## How It Works

### Content Filtering Process

1. **User submits a post/comment**
2. **AI Analysis**: The system analyzes the content using:
   - VADER Sentiment Analysis (detects positive, negative, neutral sentiment)
   - Keyword filtering (checks for cyberbullying terms)
3. **Decision Making**:
   - ✅ **Positive/Neutral content**: Posted immediately
   - ❌ **Negative/Bullying content**: Flagged and sent to admin review
4. **Admin Review**: Administrators can ban, warn, or approve flagged users/content

### Key Components

- **Sentiment Analysis**: Uses VADER (Valence Aware Dictionary and sEntiment Reasoner)
- **Keyword Detection**: Maintains a list of cyberbullying-related terms
- **User Scoring**: Tracks warning counts and user behavior
- **Admin Dashboard**: Real-time monitoring and management tools

## File Structure

```
social_media_cyberbullying_detector/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── social_media.db       # SQLite database (created automatically)
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── admin.html
│   └── profile.html
└── static/              # CSS, JavaScript, images
    ├── css/
    │   └── style.css
    └── js/
        └── main.js
```

## Usage

### For Regular Users

1. **Register** a new account or **login** with existing credentials
2. **Create posts** with positive or neutral content
3. **View your profile** and statistics
4. **Browse** other users' positive posts

### For Administrators

1. **Login** with admin credentials
2. **Access** the admin panel (`/admin`)
3. **Review** flagged accounts and content
4. **Take actions**: warn, ban, approve, or reject users/content
5. **Monitor** platform statistics

## Customization

### Adding New Cyberbullying Keywords

Edit the `CYBERBULLYING_KEYWORDS` list in `app.py`:

```python
CYBERBULLYING_KEYWORDS = [
    'hate', 'stupid', 'ugly', 'loser', 'die', 'kill',
    # Add your custom keywords here
    'newkeyword1', 'newkeyword2'
]
```

### Adjusting Sentiment Thresholds

Modify the sentiment detection logic in the `analyze_sentiment()` function:

```python
if compound >= 0.05:      # Positive threshold
    return 'positive', compound
elif compound <= -0.05:   # Negative threshold  
    return 'negative', compound
```

### Database Configuration

To use PostgreSQL or MySQL instead of SQLite, update the database URI in `app.py`:

```python
# PostgreSQL example
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/dbname'

# MySQL example  
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/dbname'
```

## Security Features

- **Password Hashing**: Uses Werkzeug for secure password storage
- **Session Management**: Flask-Login handles user sessions
- **Input Validation**: Prevents SQL injection and XSS attacks
- **Admin-only Routes**: Protected admin functionality
- **Content Sanitization**: Filters malicious content

## API Endpoints

- `GET /` - Homepage with posts
- `POST /register` - User registration
- `POST /login` - User login  
- `GET /logout` - User logout
- `POST /post` - Create new post
- `GET /admin` - Admin dashboard
- `GET /admin/review/<flag_id>/<action>` - Admin actions
- `GET /profile/<username>` - User profile

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Future Enhancements

- [ ] Machine Learning model training with custom datasets
- [ ] Multi-language support
- [ ] Image content analysis
- [ ] Real-time chat moderation
- [ ] Advanced reporting and analytics
- [ ] Mobile app development
- [ ] Integration with external moderation APIs
- [ ] User appeal system for false positives

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or contributions, please create an issue in the project repository.

---

**SafeSpace** - Building a positive online community, one post at a time! 🛡️✨
'''

with open(f'{project_name}/README.md', 'w') as f:
    f.write(readme_content)

print("Created README.md")