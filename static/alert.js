// callAlert inserts into the top of the html a bootsrap alert
function callAlert(type) {
    const divContainer = document.getElementById("burger-container");
    let alert = document.querySelector(".alert");
    let content;

    if (!alert) {
        // Depending on the type, we display different messeges
        // so the content inside alert can be modified for other uses, if required
        if (type === "login") {
            content = `
            You must have an account to buy a burger!
            <a href="/register" class="alert-link">Click here to register</a>
            or
            <a href="/login" class="alert-link">Login</a>
            `
        } else if (type === 'quantity') {
            content = `Sorry, but you can only order a maximum of 5 items!`
        }

        divContainer.insertAdjacentHTML('afterbegin', `
            <div class="alert alert-danger alert-dismissible fade show" role="alert">
                ${content}
                <button class="btn-close" aria-label="close" data-bs-dismiss="alert"></button>
            </div>
        `);
    }
}
