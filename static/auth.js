// --- SIGNUP LOGIC ---
document.getElementById('signup-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const fullName = document.getElementById('signup-name').value;
    const email = document.getElementById('signup-email').value;
    const password = document.getElementById('signup-password').value;
    const confirmPassword = document.getElementById('signup-confirm').value; // Fixed

    if (password !== confirmPassword) {
        showMessage("Passwords do not match!", "error");
        return;
    }

    const response = await fetch('http://127.0.0.1:8000/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            full_name: fullName, 
            email: email, 
            password: password 
        })
    });

    const data = await response.json();
    if (response.ok) {
        showMessage("Account created! Switching to Login...", "success");
        setTimeout(() => {
            document.getElementById('login').checked = true;
        }, 1500);
    } else {
        // Correctly parsing FastAPI detail lists
        const errorMsg = Array.isArray(data.detail) ? data.detail[0].msg : data.detail;
        showMessage(errorMsg, 'error');
    }
});

// --- LOGIN LOGIC ---
document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    const response = await fetch('http://127.0.0.1:8000/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        // Matches UserLogin schema: strictly email and password
        body: JSON.stringify({ 
            email: email, 
            password: password 
        })
    });

    const data = await response.json();
    if (response.ok) {
        // Storing the ID for relational trip creation later
        localStorage.setItem('user_id', data.user_id);
        showMessage("Login successful! Welcome back.", 'success');
        
        setTimeout(() => {
            window.location.href = "dashboard.html";
        }, 1000);
    } else {
        const errorMsg = Array.isArray(data.detail) ? data.detail[0].msg : data.detail;
        showMessage(errorMsg, 'error');
    }
});

// --- FORGOT PASSWORD MODAL LOGIC ---

// Using an event listener is more stable than .onclick
document.addEventListener('click', function (e) {
    if (e.target && e.target.classList.contains('forgot-password')) {
        e.preventDefault();
        const modal = document.getElementById('forgot-password-modal');
        if (modal) {
            modal.style.display = 'flex';
        }
    }
});

// Close Modal function
function closeModal() {
    const modal = document.getElementById('forgot-password-modal');
    if (modal) {
        modal.style.display = 'none';
    }
}

// Close modal if user clicks outside the content box
window.onclick = function(event) {
    const modal = document.getElementById('forgot-password-modal');
    if (event.target == modal) {
        closeModal();
    }
}