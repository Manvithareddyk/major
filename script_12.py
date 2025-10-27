# Create a setup script for easy installation
setup_script = '''#!/usr/bin/env python3
"""
Setup script for SafeSpace Social Media Platform
This script will set up the application and create necessary directories
"""

import os
import subprocess
import sys

def install_requirements():
    """Install Python requirements"""
    print("📦 Installing Python packages...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ Requirements installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False
    return True

def download_nltk_data():
    """Download required NLTK data"""
    print("📚 Downloading NLTK data...")
    try:
        import nltk
        nltk.download('vader_lexicon', quiet=True)
        print("✅ NLTK data downloaded successfully!")
    except Exception as e:
        print(f"❌ Error downloading NLTK data: {e}")
        return False
    return True

def create_admin_user():
    """Create initial admin user"""
    print("👤 Setting up admin user...")
    try:
        from app import app, db, User
        with app.app_context():
            db.create_all()
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                admin = User(username='admin', email='admin@example.com', is_admin=True)
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()
                print("✅ Admin user created successfully!")
                print("   Username: admin")
                print("   Password: admin123")
            else:
                print("ℹ️  Admin user already exists!")
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        return False
    return True

def main():
    """Main setup function"""
    print("🚀 Setting up SafeSpace Social Media Platform")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('app.py'):
        print("❌ Error: app.py not found. Please run this script from the project directory.")
        return False
    
    # Install requirements
    if not install_requirements():
        return False
    
    # Download NLTK data
    if not download_nltk_data():
        return False
    
    # Create admin user
    if not create_admin_user():
        return False
    
    print("=" * 50)
    print("🎉 Setup completed successfully!")
    print()
    print("To start the application:")
    print("  python app.py")
    print()
    print("Then open your browser and go to:")
    print("  http://localhost:5000")
    print()
    print("Admin login:")
    print("  Username: admin")
    print("  Password: admin123")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
'''

with open(f'{project_name}/setup.py', 'w') as f:
    f.write(setup_script)

print("Created setup.py")