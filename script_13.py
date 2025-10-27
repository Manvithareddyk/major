# Create a simple run script
run_script = '''#!/usr/bin/env python3
"""
Quick start script for SafeSpace
"""

import os
import sys

def main():
    print("🚀 Starting SafeSpace Social Media Platform...")
    
    # Check if setup has been run
    if not os.path.exists('social_media.db'):
        print("⚠️  Database not found. Running setup first...")
        os.system(f"{sys.executable} setup.py")
    
    # Start the application
    print("🌐 Starting web server...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("🔑 Admin login: admin/admin123")
    print("⛔ Press Ctrl+C to stop the server")
    print("-" * 50)
    
    os.system(f"{sys.executable} app.py")

if __name__ == "__main__":
    main()
'''

with open(f'{project_name}/run.py', 'w') as f:
    f.write(run_script)

print("Created run.py")