# Create login template
login_template = '''{% extends "base.html" %}

{% block title %}Login - SafeSpace{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card">
            <div class="card-header">
                <h3 class="text-center">
                    <i class="fas fa-sign-in-alt"></i> Login to SafeSpace
                </h3>
            </div>
            <div class="card-body">
                <form method="POST">
                    <div class="mb-3">
                        <label for="username" class="form-label">Username</label>
                        <input type="text" class="form-control" id="username" name="username" required>
                    </div>
                    <div class="mb-3">
                        <label for="password" class="form-label">Password</label>
                        <input type="password" class="form-control" id="password" name="password" required>
                    </div>
                    <div class="d-grid">
                        <button type="submit" class="btn btn-primary">
                            <i class="fas fa-sign-in-alt"></i> Login
                        </button>
                    </div>
                </form>
                <hr>
                <div class="text-center">
                    <p>Don't have an account? <a href="{{ url_for('register') }}">Register here</a></p>
                </div>
            </div>
        </div>
        
        <div class="card mt-3">
            <div class="card-body">
                <h6><i class="fas fa-info-circle"></i> Demo Account</h6>
                <p class="mb-2"><strong>Admin:</strong> admin / admin123</p>
                <small class="text-muted">Use this account to access the admin panel</small>
            </div>
        </div>
    </div>
</div>
{% endblock %}'''

with open(f'{project_name}/templates/login.html', 'w') as f:
    f.write(login_template)

print("Created templates/login.html")