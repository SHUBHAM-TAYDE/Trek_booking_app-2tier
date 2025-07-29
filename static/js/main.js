// static/js/main.js

// Function to display a message box instead of alert() - defined globally
window.showMessage = (message, type = 'success', duration = 3000) => {
    let messageBox = document.getElementById('messageBox');
    if (!messageBox) {
        messageBox = document.createElement('div');
        messageBox.id = 'messageBox';
        messageBox.className = 'message-box';
        document.body.appendChild(messageBox);
    }

    messageBox.textContent = message;
    messageBox.className = 'message-box show'; // Reset classes
    if (type === 'error') {
        messageBox.classList.add('error');
    } else {
        messageBox.classList.remove('error');
    }

    setTimeout(() => {
        messageBox.classList.remove('show');
        // Optional: Remove the element after transition for cleanup
        setTimeout(() => {
            messageBox.style.display = 'none';
        }, 500); // Match transition duration
    }, duration);
};


document.addEventListener('DOMContentLoaded', () => {
    // Define API_BASE_URL to explicitly target the Flask backend
    const API_BASE_URL = 'http://127.0.0.1:5000';

    // Function to update login/logout button and display username
    const updateAuthUI = async () => {
        const loginLink = document.getElementById('login-link');
        const logoutButton = document.getElementById('logout-button');
        const usernameDisplay = document.getElementById('username-display');

        try {
            // Use API_BASE_URL to make the URL absolute
            const response = await fetch(`${API_BASE_URL}/api/user_status`);
            const data = await response.json();

            if (data.logged_in) {
                if (loginLink) loginLink.classList.add('hidden');
                if (logoutButton) logoutButton.classList.remove('hidden');
                if (usernameDisplay) {
                    usernameDisplay.textContent = `Welcome, ${data.username}!`;
                    usernameDisplay.classList.remove('hidden');
                }
            } else {
                if (loginLink) loginLink.classList.remove('hidden');
                if (logoutButton) logoutButton.classList.add('hidden');
                if (usernameDisplay) usernameDisplay.classList.add('hidden');
            }
        } catch (error) {
            console.error('Error fetching user status:', error);
            // Default to logged out state on error
            if (loginLink) loginLink.classList.remove('hidden');
            if (logoutButton) logoutButton.classList.add('hidden');
            if (usernameDisplay) usernameDisplay.classList.add('hidden');
        }
    };

    // Attach logout functionality
    const logoutButton = document.getElementById('logout-button');
    if (logoutButton) {
        logoutButton.addEventListener('click', async () => {
            try {
                // Use API_BASE_URL to make the URL absolute
                const response = await fetch(`${API_BASE_URL}/api/logout`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
                const data = await response.json();
                if (response.ok) {
                    showMessage(data.message, 'success');
                    updateAuthUI(); // Update UI after logout
                    // Redirect to home or login page after logout
                    window.location.href = '/';
                } else {
                    showMessage(data.message, 'error');
                }
            } catch (error) {
                console.error('Logout error:', error);
                showMessage('An error occurred during logout.', 'error');
            }
        });
    }

    // Call on page load to set initial auth state
    updateAuthUI();
});
