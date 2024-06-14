const ORDER_LIMIT = 5;

// We make cartAmount a global variable as it is used by multiple function
let cartAmount = document.getElementById('order-number'); // We use 'let' since the cartAmount value may change dynamically, and we need to capture and use the updated value.

function updateOrder(event, orderId) {
    // Get the cart amount
    let newCartAmount = parseInt(cartAmount.textContent);

    // Get order amount
    const quantityTag = document.getElementById(`quantity-${orderId}`);
    let newQuantity = parseInt(quantityTag.innerText);

    // Update order amount and cart in the HTML
    if (event === 'add' && newQuantity < ORDER_LIMIT) {
        newQuantity++;
        newCartAmount++;
    } else if (event == 'substract' && newQuantity > 1) {
        newQuantity--;
        newCartAmount--;
    }
    // Although we change it to a trash icon, it still functions as a substract button
    // if the substraction is equal to zero we call deleteItem to confirm deletion of item
    else if ((newQuantity - 1) === 0) {
        deleteItem(orderId, newCartAmount);
    }
    // In the case the user tries to add more than the ORDER_LIMIT
    else {
        return callAlert('quantity');
    }

    // Reflect the change of quantity in the order and cart
    quantityTag.innerHTML = newQuantity;
    cartAmount.innerHTML = newCartAmount;

    // Update '-' icon
    toggleTrashIcon();

    // Calculate the total order price
    calculateTotal();

    // Disable / enable clear order modal
    toggleClearOrderBtn()

    // Update Session
    updateUserOrder(orderId, newQuantity);
}


// Use fetch to prevent page from reloading everytime the user wants to add or substract from his order
function updateUserOrder(orderId, newQuantity) {
    const data = JSON.stringify({
        orderId: orderId,
        quantity: newQuantity
    });
    fetch('/order', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: data,
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Server response:', data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}


function deleteItem(orderId, newCartAmount) {
    // Toggle Modal
    const deleteItemModal = document.getElementById('delete-item-modal');
    let modal = new bootstrap.Modal(deleteItemModal);
    modal.show();

    // Get element and remove it from html
    document.getElementById('del-item-button').addEventListener('click', function() {
        document.getElementById(orderId).remove();
        // Update cart, total amount and backend

        newCartAmount--;
        cartAmount.innerHTML = newCartAmount;

        toggleClearOrderBtn();
        calculateTotal();
        updateUserOrder(orderId, 0);
    });
}


function toggleTrashIcon() {
    // Query through all orders
    document.querySelectorAll('.card').forEach(function(element, index) {
        // Get the amount of each order
        const quantity = element.querySelector('[id^="quantity-"]').textContent;
        let substractButton = element.querySelector('[id^="substract-"]');

        // If the amount is equal to 1 we change the icon to a trash can
        if (quantity == 1) {
            substractButton.innerHTML = '<i class="bi bi-trash"></i>';
        }
        // else we replace it with a minus symbol
        else {
            substractButton.innerHTML = "-";
        }
    });
}


function calculateTotal() {
    let total = 0.00;

    document.querySelectorAll('.card').forEach(function(element, index) {
        // Get the amount of each item
        let amount = element.querySelector('[id^="quantity-"]');
        amount = parseFloat(amount.textContent);

        // Get the price of each item
        let price = element.querySelector('.item-price');
        price = parseFloat(price.textContent.replace("$", ""));

        // Calculate total
        total += amount * price;
    });

    // Update value in HTML
    document.querySelector('.float-end').innerHTML = `$${total.toFixed(2)}`;
}


function clearOrderModal() {
    // Loop though all the orders and remove them from the html
    document.querySelectorAll('.card').forEach(function(element, index) {
        element.remove();
    });
}


function toggleClearOrderBtn() {
    const openModalButton = document.querySelector('.btn-link');

    // We select all the orders
    // if the order is empty, querySelectorAll returns a NodeList with a length of 0
    if (document.querySelectorAll('.card').length === 0) {
        // In that case we disable the clear order button
        return openModalButton.disabled = true;
    }
    // else we enable the button
    return openModalButton.disabled = false;
}


document.addEventListener('DOMContentLoaded', function() {
    // When the page is loaded we make sure to update values:
    toggleTrashIcon(); // to show trash icon or ' - ',
    calculateTotal(); // Calculate the current total ,
    toggleClearOrderBtn(); // Check if the clear order button should be enabled.
});

document.getElementById('clear-order-button').addEventListener('click', function() {
    // If the clear order button in the modal is clicked,
    cartAmount.innerHTML = 0; // update cart
    clearOrderModal(); // Remove all orders from html
    calculateTotal(); // Calculate new total
    toggleClearOrderBtn(); // Disable clear order button
    updateUserOrder('clear-order', 0); // Update backend with specialy key ('clear-order') that eliminates all user orders in python backend
});
