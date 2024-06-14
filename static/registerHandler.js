// Makes use of bootsrap form validation to toggle between css classes
const form = document.querySelector("form");

form.addEventListener('submit', function(event) {
    const inputs = document.querySelectorAll("input");
    const password = document.getElementById("password");
    const confirmPassword = document.getElementById("confirm-password");

    // Unlike formHandler.js, we cant simply rely on checkValidty
    // Added specfic validation to check if the passwrod is 8 characters long and if it matches confirmPassword
    if (!form.checkValidity() || password.value.length < 8 || confirmPassword.value != password.value) {
        event.preventDefault();

        inputs.forEach(input => {
            toggleIsValidClass(input, input.checkValidity() ? "is-valid" : "is-invalid");
        });

        toggleIsValidClass(confirmPassword, confirmPassword.value === password.value && password.value !== "" ? "is-valid" : "is-invalid");

        const passwordValid = password.value.length >= 8;

        toggleIsValidClass(password, passwordValid ? "is-valid" : "is-invalid");
    }
});
