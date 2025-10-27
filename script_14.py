# Create a configuration file for easy customization
config_py = '''"""
Configuration settings for SafeSpace Social Media Platform
Modify these settings to customize the application behavior
"""

import os

class Config:
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-this-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///social_media.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Application Settings
    POSTS_PER_PAGE = 20
    MAX_CONTENT_LENGTH = 500  # Maximum characters per post
    
    # Cyberbullying Detection Settings
    CYBERBULLYING_KEYWORDS = [
        'hate', 'stupid', 'ugly', 'loser', 'die', 'kill', 'worthless', 'pathetic',
        'dumb', 'idiot', 'shut up', 'go away', 'nobody likes you', 'freak', 'weirdo',
        'fat', 'disgusting', 'trash', 'garbage', 'failure', 'useless'
    ]
    
    # Sentiment Analysis Thresholds
    POSITIVE_THRESHOLD = 0.05    # Compound score >= this value = positive
    NEGATIVE_THRESHOLD = -0.05   # Compound score <= this value = negative
    VERY_NEGATIVE_THRESHOLD = -0.5  # Threshold for automatic flagging
    
    # Admin Settings
    AUTO_BAN_WARNING_COUNT = 5   # Auto-ban users after this many warnings
    REQUIRE_EMAIL_VERIFICATION = False  # Set to True to require email verification
    
    # Security Settings
    MAX_LOGIN_ATTEMPTS = 5       # Maximum login attempts before lockout
    LOCKOUT_DURATION = 300       # Lockout duration in seconds (5 minutes)
    
    # UI Settings
    THEME_COLOR = '#007bff'      # Primary theme color
    ITEMS_PER_ADMIN_PAGE = 50    # Items to show per page in admin panel

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = False  # Set to True to see SQL queries

class ProductionConfig(Config):
    DEBUG = False
    # In production, use environment variables for sensitive data
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

# Choose configuration based on environment
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
'''

with open(f'{project_name}/config.py', 'w') as f:
    f.write(config_py)

print("Created config.py")