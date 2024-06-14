// Makes use of bootsrap form validation to toggle between css classes
const form = document.querySelector("form");

form.addEventListener("submit", function(event) {
    if (!form.checkValidity()) {
        event.preventDefault()
    }
    form.classList.add("was-validated")
});
