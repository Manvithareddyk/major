# Create index template
index_template = '''{% extends "base.html" %}

{% block title %}Home - SafeSpace{% endblock %}

{% block content %}
<div class="row">
    <div class="col-md-8">
        <h2>Welcome to SafeSpace</h2>
        <p class="text-muted">A social platform that promotes positive interactions and prevents cyberbullying</p>
        
        {% if current_user.is_authenticated %}
            <div class="card mb-4">
                <div class="card-header">
                    <h5>Create a Post</h5>
                </div>
                <div class="card-body">
                    <form method="POST" action="{{ url_for('create_post') }}">
                        <div class="mb-3">
                            <textarea class="form-control" name="content" rows="3" 
                                    placeholder="Share something positive..." required></textarea>
                        </div>
                        <button type="submit" class="btn btn-primary">
                            <i class="fas fa-paper-plane"></i> Post
                        </button>
                    </form>
                </div>
            </div>
        {% endif %}

        <div class="posts">
            {% if posts %}
                {% for post in posts %}
                    <div class="card mb-3">
                        <div class="card-body">
                            <div class="d-flex justify-content-between align-items-start mb-2">
                                <h6 class="card-title">
                                    <a href="{{ url_for('profile', username=post.author.username) }}" 
                                       class="text-decoration-none">
                                        <i class="fas fa-user-circle"></i> {{ post.author.username }}
                                    </a>
                                </h6>
                                <small class="text-muted">{{ post.created_at.strftime('%Y-%m-%d %H:%M') }}</small>
                            </div>
                            <p class="card-text">{{ post.content }}</p>
                            {% if post.sentiment_label %}
                                <span class="badge bg-{{ 'success' if post.sentiment_label == 'positive' else 'secondary' }}">
                                    {{ post.sentiment_label.title() }}
                                </span>
                            {% endif %}
                        </div>
                    </div>
                {% endfor %}
            {% else %}
                <div class="text-center py-5">
                    <i class="fas fa-comments fa-3x text-muted mb-3"></i>
                    <h4>No posts yet</h4>
                    <p class="text-muted">Be the first to share something positive!</p>
                </div>
            {% endif %}
        </div>
    </div>
    
    <div class="col-md-4">
        <div class="card">
            <div class="card-header">
                <h5><i class="fas fa-shield-alt"></i> Community Guidelines</h5>
            </div>
            <div class="card-body">
                <ul class="list-unstyled">
                    <li><i class="fas fa-heart text-danger"></i> Be kind and respectful</li>
                    <li><i class="fas fa-smile text-warning"></i> Share positive content</li>
                    <li><i class="fas fa-ban text-danger"></i> No hate speech or bullying</li>
                    <li><i class="fas fa-users text-primary"></i> Support each other</li>
                </ul>
                <small class="text-muted">
                    Our AI system automatically filters negative content to maintain a safe environment.
                </small>
            </div>
        </div>

        {% if current_user.is_authenticated %}
            <div class="card mt-3">
                <div class="card-header">
                    <h5><i class="fas fa-user"></i> Your Stats</h5>
                </div>
                <div class="card-body">
                    <p><strong>Posts:</strong> {{ current_user.posts|length }}</p>
                    <p><strong>Warnings:</strong> 
                        <span class="badge bg-{{ 'danger' if current_user.warning_count > 0 else 'success' }}">
                            {{ current_user.warning_count }}
                        </span>
                    </p>
                    <p><strong>Status:</strong> 
                        <span class="badge bg-{{ 'danger' if current_user.is_banned else 'success' }}">
                            {{ 'Banned' if current_user.is_banned else 'Active' }}
                        </span>
                    </p>
                </div>
            </div>
        {% endif %}
    </div>
</div>
{% endblock %}'''

with open(f'{project_name}/templates/index.html', 'w') as f:
    f.write(index_template)

print("Created templates/index.html")