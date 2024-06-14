// Image URL validator made by chatGPT
function isImageUrl(url) {
    // Regular expression to match common image file extensions
    const imageExtensions = /\.(jpeg|jpg|gif|png|bmp|svg)$/i;

    // Check if the string is a valid URL and has a matching image file extension
    return /^(http|https):\/\/\S+\.\S+$/.test(url) || imageExtensions.test(url);
  }

const form = document.querySelector("form");

form.addEventListener('submit', function() {
    const inputs = document.querySelectorAll("input");
    const imageURL = document.getElementById("image-url");
    const description = document.getElementById("description");
    const category = document.getElementById("category");

    const isOptionDisabled = category.options[category.selectedIndex].disabled;

    if (!form.checkValidity() || !isImageUrl(imageURL.value) || isOptionDisabled) {
        event.preventDefault();

        inputs.forEach(input => {
            toggleIsValidClass(input, input.checkValidity() ? "is-valid" : "is-invalid");
        });

        toggleIsValidClass(imageURL, isImageUrl(imageURL.value) ? 'is-valid' : 'is-invalid');

        toggleIsValidClass(description, description.checkValidity() ? 'is-valid' : 'is-invalid');

        toggleIsValidClass(category, !isOptionDisabled  ? 'is-valid' : 'is-invalid');
    }
});
