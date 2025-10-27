# Create requirements.txt
requirements_content = '''Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-Login==0.6.3
Werkzeug==2.3.7
vaderSentiment==3.3.2
'''

with open(f'{project_name}/requirements.txt', 'w') as f:
    f.write(requirements_content)

print("Created requirements.txt")