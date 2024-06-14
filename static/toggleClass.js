// toggleIsValidClass toggles elements class between 'is-valid' and 'is-invalid'
function toggleIsValidClass(element, className) {
    element.classList.toggle("is-valid", className === "is-valid");
    element.classList.toggle("is-invalid", className === "is-invalid");
}
