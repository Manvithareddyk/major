"""
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
        # English & general
        'hate', 'stupid', 'ugly', 'loser', 'die', 'kill', 'worthless', 'pathetic',
        'dumb', 'idiot', 'shut up', 'go away', 'nobody likes you', 'freak', 'weirdo',
        'fat', 'disgusting', 'trash', 'garbage', 'failure', 'useless',
        # Vulgar, sexual, explicit, harassment
        'bitch', 'bastard', 'sex', 'ass', 'c', 'randi', 'rape', 'rapist', 'molest', 
        'molestation', 'pedophile', 'grooming', 'harass', 'harassment', 'sexual', 'fuck', 
        'fucker', 'slut', 'whore', 'prostitute', 'escort', 'hoe', 'suck', 'cocksucker',
        'strip', 'nude', 'porn', 'sleep with you', 'rate per day', 'price per day',
        'pay for sex', 'daddy issues', 'open for sex', 'come to my room', 'cheap girl',
        # Violence/threats
        'violence', 'fight', 'beat', 'attack', 'stab', 'shoot', 'blood', 'killer', 
        'murder', 'hurt you', 'I will kill you', 'wish you were dead',
        # Romanized Hindi/Slang
        'madrchod', 'bhenchod', 'chutiya', 'gandu', 'gaand', 'lodu', 
        'saala', 'haraami', 'kutte', 'mar ja', 'bakchod', 'fattu', 'befikar', 
        'bekar', 'nalayak', 'ghatiya', 'murkha', 'bekaar', 'bhosdike', 'bhaag ja',
        # Hindi Devanagari
        'मूर्ख', 'घृणा', 'गंदा', 'नालायक', 'मर जा', 'फालतू', 'बेकार', 'रंडी',
        # Spanish
        'estúpido', 'odio', 'feo', 'perdedor', 'muérete', 'basura', 'despreciable', 'puta', 'gilipollas', 'imbécil',
        # Arabic
        'حقير', 'غبي', 'أكرهك', 'قبيح', 'لا أحد يحبك', 'مقرف', 'عاهرة',
        # Urdu (Roman and script)
        'Harami', 'Kamina', 'Chutiya', 'Beghairat', 'Kutta', 'Randi', 'کنجر', 'حرامی', 'کمینہ', 'چوتیا', 'بےغیرت', 'کتا', 'رنڈی',
        # Turkish
        'orospu', 'aptal', 'salak', 'gerizekalı', 'yavşak', 'hayvan', 'şerefsiz', 'amcık', 'hain',
        # Japanese (hiragana, katakana, kanji and romaji)
        'バカ', '死ね', 'くそ', 'あほ', 'デブ', 'だまれ', '殺す', 'ばかやろう', 'kusogaki', 'shine',
        # Korean (Hangul, romanized)
        '바보', '멍청이', '씨발', '죽어', '꺼져', '빙신', '쓸모없다', '시발', 'jeongmal', 'ssibal',
        # Common abuser emojis
        '💩', '🤡', '🖕', '😡', '👎', '🍑', '🍆',()()
        # Add more, expand and update as needed per community usage!
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
