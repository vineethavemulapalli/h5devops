document.getElementById('registrationForm').addEventListener('submit', function(e) {
    // Stop the form from refreshing the page
    e.preventDefault();

    // Get form values
    const fullName = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    // 1) Check password length
    if (password.length < 6) {
        alert("Password must be at least 6 characters long.");
        return; // Stop further execution
    }

    // 2) Check password match
    if (password !== confirmPassword) {
        alert("Passwords do not match!");
        return; // Stop further execution
    }

    // 3) If all good, display only Full Name & Email
    alert(
        "Full Name: " + fullName + "\n" +
        "Email: " + email
    );
});
