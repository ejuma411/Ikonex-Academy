// Session timeout warning (shows 30 seconds before logout)
let timeoutWarning;

function startSessionTimer() {
    // 4 minutes 30 seconds (270 seconds) - show warning 30 seconds before logout
    timeoutWarning = setTimeout(function() {
        showSessionWarning();
    }, 270000);
}

function showSessionWarning() {
    if (confirm('You will be logged out in 30 seconds due to inactivity. Click OK to stay logged in.')) {
        // Reset session by making a request to the server
        fetch('/refresh-session/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json',
            },
        }).then(function(response) {
            if (response.ok) {
                resetTimer();
            }
        });
    } else {
        // User didn't respond - let session expire naturally
        clearTimeout(timeoutWarning);
    }
}

function resetTimer() {
    clearTimeout(timeoutWarning);
    startSessionTimer();
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Track user activity
document.addEventListener('click', resetTimer);
document.addEventListener('keypress', resetTimer);
document.addEventListener('mousemove', resetTimer);
document.addEventListener('scroll', resetTimer);

// Auto-dismiss messages after 4 seconds
document.addEventListener('DOMContentLoaded', function() {
    const messages = document.querySelectorAll('.alert');
    messages.forEach(function(message) {
        setTimeout(function() {
            message.style.transition = 'opacity 0.5s';
            message.style.opacity = '0';
            setTimeout(function() {
                message.remove();
            }, 500);
        }, 4000); // 4 seconds
    });
});

// Start timer on page load
startSessionTimer();