# Create JavaScript file
js_content = '''// Main JavaScript file for SafeSpace
document.addEventListener('DOMContentLoaded', function() {
    
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Form submission loading state
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.innerHTML = '<span class="spinner"></span> Processing...';
                submitBtn.disabled = true;
            }
        });
    });
    
    // Confirm dialogs for admin actions
    const dangerLinks = document.querySelectorAll('a.btn-danger');
    dangerLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            if (!link.onclick) { // Only if no existing onclick handler
                if (!confirm('Are you sure you want to perform this action?')) {
                    e.preventDefault();
                    return false;
                }
            }
        });
    });
    
    // Character counter for post content
    const postTextarea = document.querySelector('textarea[name="content"]');
    if (postTextarea) {
        const maxLength = 500;
        const counter = document.createElement('small');
        counter.className = 'text-muted';
        counter.style.float = 'right';
        postTextarea.parentNode.appendChild(counter);
        
        function updateCounter() {
            const remaining = maxLength - postTextarea.value.length;
            counter.textContent = remaining + ' characters remaining';
            counter.className = remaining < 50 ? 'text-danger' : 'text-muted';
        }
        
        postTextarea.addEventListener('input', updateCounter);
        postTextarea.maxLength = maxLength;
        updateCounter();
    }
    
    // Real-time content analysis preview
    if (postTextarea) {
        const previewDiv = document.createElement('div');
        previewDiv.className = 'mt-2';
        previewDiv.id = 'content-preview';
        postTextarea.parentNode.appendChild(previewDiv);
        
        postTextarea.addEventListener('input', function() {
            const content = this.value.toLowerCase();
            const warningWords = ['hate', 'stupid', 'ugly', 'loser', 'die', 'kill'];
            const hasWarningWords = warningWords.some(word => content.includes(word));
            
            if (hasWarningWords && content.length > 10) {
                previewDiv.innerHTML = '<div class="alert alert-warning alert-sm py-2"><i class="fas fa-exclamation-triangle"></i> Your content may be flagged for review.</div>';
            } else if (content.length > 10) {
                previewDiv.innerHTML = '<div class="alert alert-success alert-sm py-2"><i class="fas fa-check"></i> Content looks positive!</div>';
            } else {
                previewDiv.innerHTML = '';
            }
        });
    }
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Toast notifications
    function showToast(message, type = 'info') {
        const toastContainer = document.getElementById('toast-container') || createToastContainer();
        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-white bg-${type} border-0`;
        toast.setAttribute('role', 'alert');
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;
        toastContainer.appendChild(toast);
        
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
        
        toast.addEventListener('hidden.bs.toast', function() {
            toast.remove();
        });
    }
    
    function createToastContainer() {
        const container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        document.body.appendChild(container);
        return container;
    }
    
    // Make showToast globally available
    window.showToast = showToast;
    
    // Add loading state to navigation links
    const navLinks = document.querySelectorAll('.navbar-nav a.nav-link');
    navLinks.forEach(function(link) {
        link.addEventListener('click', function() {
            const icon = this.querySelector('i');
            if (icon && !icon.classList.contains('fa-spin')) {
                icon.classList.add('fa-spin');
                setTimeout(() => icon.classList.remove('fa-spin'), 1000);
            }
        });
    });
});

// Utility functions
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        showToast('Copied to clipboard!', 'success');
    });
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' at ' + date.toLocaleTimeString();
}

// Initialize tooltips if Bootstrap is available
document.addEventListener('DOMContentLoaded', function() {
    if (typeof bootstrap !== 'undefined') {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        const tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
});'''

with open(f'{project_name}/static/js/main.js', 'w') as f:
    f.write(js_content)

print("Created static/js/main.js")