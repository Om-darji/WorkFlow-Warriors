// --- PHOTO PREVIEW ---
document.getElementById('signup-photo')?.addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(event) {
            const preview = document.getElementById('photo-preview');
            preview.innerHTML = `<img src="${event.target.result}" alt="Profile Photo">`;
        };
        reader.readAsDataURL(file);
    }
});

// --- SIGNUP LOGIC ---
document.getElementById('signup-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const fullName = document.getElementById('signup-name').value;
    const email = document.getElementById('signup-email').value;
    const phone = document.getElementById('signup-phone').value;
    const city = document.getElementById('signup-city').value;
    const country = document.getElementById('signup-country').value;
    const password = document.getElementById('signup-password').value;
    const confirmPassword = document.getElementById('signup-confirm').value;
    const additionalInfo = document.getElementById('signup-additional-info').value;

    if (password !== confirmPassword) {
        showMessage("Passwords do not match!", "error");
        return;
    }

    const response = await fetch('/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            full_name: fullName, 
            email: email,
            phone_number: phone,
            city: city,
            country: country,
            password: password,
            additional_info: additionalInfo
        })
    });

    const data = await response.json();
    if (response.ok) {
        showMessage("Account created! Please login.", "success");
        setTimeout(() => {
            // This triggers the CSS transition in your login.css
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

    const response = await fetch('/login', {
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
            window.location.href = "landing.html";
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

function showMessage(text, type) {
    const box = document.getElementById('message-box');
    if (!box) {
        // Fallback if the message-box div is missing from HTML
        alert(text);
        return;
    }
    box.innerText = text;
    box.className = type === 'error' ? 'hidden-msg msg-error' : 'hidden-msg msg-success';
    
    // Hide it after 3 seconds
    setTimeout(() => {
        box.className = 'hidden-msg';
    }, 3000);
}