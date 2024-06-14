// CategoryHandler filters items in menu.html and items.html by their category (Burgers, Sides, Beverages, Desserts)
document.getElementById("category-filter").addEventListener('change', function() {
    const selectedCategory = this.value;
    displaySelectedItems(selectedCategory);
});

// Gets the category selected by the user and loops through all menu items
function displaySelectedItems(selectedCategory) {
    const menuItems = document.getElementsByClassName('col-menu-item');

    for (let i = 0; i < menuItems.length; i++) {
        // All menu items have a data-category atribbute were the category of the item is saved
        const itemCategory = menuItems[i].getAttribute('data-category');

        // If it matches then we display it, else we dont
        if (selectedCategory === 'all' || itemCategory === selectedCategory) {
            menuItems[i].style.display = "block";
        } else {
            menuItems[i].style.display = "none";
        }
    }
}
