// --- SIGNUP LOGIC ---
document.getElementById('signup-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const fullName = document.getElementById('signup-name').value;
    const email = document.getElementById('signup-email').value;
    const password = document.getElementById('signup-password').value;

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
        alert("Account created! You can now login.");
        document.getElementById('login').checked = true; // Switch tab to Login
    } else {
        alert("Signup Error: " + data.detail);
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
        body: JSON.stringify({ email: email, password: password })
    });

    const data = await response.json();
    if (response.ok) {
        // IMPORTANT: Store the user_id so we know who is logged in!
        localStorage.setItem('user_id', data.user_id);
        alert("Login successful!");
        window.location.href = "dashboard.html"; // Redirect to next screen
    } else {
        alert("Login Error: " + data.detail);
    }
});