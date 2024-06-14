 # BURGER SHOP
#### Video Demo:  <[Final Project Video Demo](https://youtu.be/75O070MF3OE)>
#### Description:
Burger Shop is a web app, whose main objective is to facilitate managing your own restaurant web page. As administrators, owners can add, edit or remove items from the page. Each product can be customized with their own name, description, price, image and categories (Burgers, Sides, Beverages and desserts). They can also add other administrators (from a list of registered users) or remove them. On the other hand, users can use the categories to filter their search, add items to their cart, remove or increase the amount of each order and finally, fill in their billing information in checkout.

## /project files

Inside  the project folder will find 2 folders (*static* and *templates*) and 3 important files (*burger_data.db*, *helpers.py* and *app.py*).

### burger_data.db
Contains 5 tables that hold all of the data that a burger shop will need. This are:
* **users** Stores all registered users and their password formatted into a hash.
* **menu** Stores all the menu items, including their name, description, price, category id and a image URL
* **categories** Stores food categories, which i've set by default to 4 different kinds: burgers, sides, beverages and desserts.
* **user_order** Stores the amount of each of the items the user added to his order.
* **admins** Stores the registered accounts that have access to administrator functionalities.

**Note**
At first, the categories were simply stored in each of the menu items, but I later decided to separate it to its own table as it was better when showing the category selector, when editing, adding or filtering the search, to loop through all of the categories in the categories table. Otherwise I would have to write it manually and if the owner decided to modify one of these they would have to go to each place where categories are used.


### helpers.py
*helpers.py* contains 2 of the functions from *C$50 Finance*; **apology()**, which renders a page with a custom error message, and **login_required()**, a decorated function that keeps users out of the desired page if they are not logged in. But, I have added 3 function of my own:
* **admin_required** works just as *login_required* but for keeping non-admin users from desired pages, by querying for the *admins* table
* **add_edit_items** is used in the admin routes to add or edit items from the menu. The logic for editing and adding are almost the same, apart from the sql query. The function accepts a type parameter. If it's “edit” it will UPDATE the table, if it's “add”, it will INSERT INTO the table, only if all fields are completed.
* *return_usa_states* simply returns all the states in the USA. This is used when the user is in the checkout, and has to select where he wants his order shipped to. This could be modified, by the owner, depending on the restaurant's availability in each state.


### app.py
In *app.py* we set up our flask app, import the necessary libraries, connect SQLite to use burger_data.db and  create our 5 tables as detailed above. Moreover, we configure a context processor. This is crucial as the navigation bar needs to monitor the user's order count, if any, and determine whether the user is an administrator to decide whether to display the admin navigation links. And a small note, we define a global variable *ORDER_LIMIT* to establish a reasonable limit of how many of each item the user can order.
*app.py* handles 16 routes.

**"Open access for all."**
* /register
* /login
* /logout
* /
* /menu

**Must be logged in**
* /burger/<int:burger_id>
* /order
* /checkout
* /order-succesful

**Must be administrator **
* /admin-items
* /admin-items/delete/<int:burger_id>
* /admin-items/edit/<int:burger_id>
* /admin-items/add
* /admin-users
* /admin-users/delete/<int:admin_id>
* /admin-users/add

Before delving into the specifics of each route within app.py, well talk two files inside the *templates* folder: *layout.html* and *confirm-modal.html*

### layout.html
Before delving into the specifics of each route within app.py, it's essential to highlight the significance of /templates/layout.html. This file serves as the cornerstone, dictating the comprehensive structure and layout of every web page. Noteworthy components of this layout include:
* Bootstrap Navbar: Seamlessly integrating a Bootstrap navbar, *layout.html* ensures an intuitive and navigable interface. This navbar is designed with responsiveness in mind, adeptly adjusting to diverse screen sizes for an optimal user experience.
* Dynamic Adaptation: A distinctive feature lies in the adaptive nature of the navbar. It dynamically tailors its content based on the user's status – whether they are not logged in, logged in, or hold administrator privileges. This responsive behavior ensures a personalized and contextually relevant display.
* Cart Display: This feature prominently showcases the total amount of the user's current order. Providing users with instant visibility into their order status.
* Footer: Completing the layout is a footer section, contributing to the overall cohesion and polished appearance of the web pages.

By centralizing these essential elements within layout.html, the web pages maintain a unified design language and ensures consistency across the entire application.

### confirm-modal.html
*confirm-modal* is a Bootstrap modal designed as a versatile template for confirming various user actions. To tailor the modal to specific needs, customization options include the modal header, description, and a unique ID for the modal and the confirm button, crucial for identification and triggering through JavaScript. Alongside the header and description, the modal features a close button (X) at the top right and a cancel button for convenient closure (clicking outside the modal achieves the same). The confirmation button is included for users to affirm their decisions, and its functionality is determined by the corresponding JavaScript code.


## Routes

### /register
**/templates/register.html** showcases a form featuring three mandatory fields: email, password, and confirm password. Beyond backend validation, I've implemented fundamental validation using JavaScript and Bootstrap. This dual-layered validation mechanism prevents the form from submitting prematurely. Instead, users receive real-time feedback on erroneous fields, enhancing the overall user experience by providing clarity and immediate guidance in case of inaccuracies.

**register()** handles field validation, including an email validator from the *email_validator* library. If all fields are valid, the password is hashed using *werkzeug.security* library and saved into the *users* table. We then create a session for the user and redirect him to the homepage.


### /login /logout
**/templates/login.html.html** displays a form with two fields; email and password. Just as *register.html*, it contains frontend validation.
**login()** and **logout()** remains unchanged from *C$50 Finance*.


### /
**/templates/index.html** displays a generic promotional video, showing a chef making a burger. This video was made by [hzsphoto](https://www.youtube.com/watch?v=VQmT5h7m3q4&ab_channel=hzsphoto)

**index()** simply renders *index.html*


### /menu
**/templates/menu.html** displays all of the items stored in the *menu* table, showcasing the product name, image and price. The items are arranged in card format, with a maximum of 2 cards per row. However, for smaller screens, a single item per row is displayed. The page also offers users filtering their search by categories, positioned at the top of the screen.

**menu()** simply queries the database to get two tables; *menu* and *categories*, and passes it to *menu.html* when it is rendered.


### /burger/<int:burger_id>
**/templates/burger-detail.html** displays the specific item clicked by the user in *menu.html*. In addition to the name, image and price, we are also shown a brief description of the item. At the bottom will find a “buy” button. If the user is not logged in, the button will be disabled and trigger a bootstrap alert, notifying the user that they must log in to buy an item.

**burger_detail(burger_id)** expects a **burger_id**, stored in each form in *menu.html*, to query the *menu* table. The retrieved information is then passed as a parameter to *burger-detail.html* for accurate item display. Additionally, *userIsLoggedIn* is passed to *burger-detail.html* to dynamically enable or disable the buy button. If the user is logged in and clicks the buy button, a post request is triggered. This request adds the item to the cart only if it doesn't exceed the ORDER_LIMIT. In case the item is already in the user's cart, we simply update the quantity in the *user_order* table. Following this, the user is seamlessly redirected to */order*.


### /order
**/templates/order.html** displays all of the users order, showing a small image of the product, name, price, amount and the sum total. The user also has a ‘+’ and ‘-’ buttons, that allow him to modify the order amount of each item. If the amount is 1, the ‘-’ will be replaced with a bootstrap trash icon, which will trigger *confirm-modal.html*, asking the user to confirm the deletion. Trying to add more than 5 items will prompt a bootsrap alert, informing the user about the order limit. In addition, there is a ‘clear order’ button at the top right, which will allow you to delete all of the items in the order, and just as before, *confirm-modal.html* will pop up, asking you to confirm your action. Modifying the amount and clearing the order is done asynchronously (by *orderHandler.js*) , to prevent the page from reloading and provide a better user experience.

**order()** queries *user_order* to retrive all of the orders from the user and pass them to *order_html*. Upon receiving a POST request, the code checks for the triggering event. If the event corresponds to the ‘clear order’ button, all user orders in *user_order* are deleted.  In the case of a change in the order amount, we simply update *user_order*. If the trash icon is clicked, the order amount will equal 0. In that case the corresponding item is deleted from *user_order*.


### /checkout
**/templates/checkout.html** displays one form for billing information, which includes:
* first name
* last name
* street address
* city
* state (dropdown menu that gets an array of states from *return_usa_states()*)
* zip code
* payment method (dropdown menu. Has three hard coded card: Mastercard, Visa and American Express)
* card number
* expiration month (which uses a simple loop to display months 1 to 12)
* expiration year (which shows the current year and extends the options 26 years into the future)
* security code

Moreover, the page includes an order summary within a card form, mirroring the information found in *order.html* (name, quantity, price, total). However, this summary lacks the interactive functionalities present in *order.html*. Its role is to offer users a detailed overview of their selected items before they proceed to finalize the purchase.

**checkout()** renders *checkout.html* and pass important parameters: The **current_year**, by importing *datetime*. The corresponding users **order** form *user_order*, **return_usa_states()** from *helpers.py* and the **total**, which we calculate by summing all of the users orders from *user_order*, multiplying the price by the amount. Unlike *order.html*, which calculates the total in the front-end, I decided to calculate it in the backend to ensure that the server has control over the critical financial calculations, avoiding any discrepancies between the frontend and backend. In addition, I prevent users from reaching */checkout* if their order is empty.


### /order-successful
**/templates/order-successful.html** displays a simple message to communicate to the user that the order was successful and its on its way. It provides a button that will redirect the user back to the homepage.

**order_succesful()** renders *order-succesful.html* only if all the fields required are filled and the card number, expiration year and month  is valid. I used the card validator from the *sentimental-credit* problem set, with some modifications, to make sure the user inputs an official card. It also checks the security code length, as Mastercard and visa cards use 3 digits and Amex 4. Furthermore, I check the validity of the expiration month and year, making sure they don't select a month that does not exist or an expiration year that is smaller than the current year. If any validation fails, an *apology()* is returned. Finally, as an extra measure of security, the page is only accessible through a POST request, preventing users from bypassing *checkout.html*. Otherwise, they will be redirected to the homepage.


### /admin-items
**/templates/admin/items.html** similar to *menu.html*, but each of the cards now show two buttons; edit and delete, with the respective items ID embedded. Deleting an item will pop up the *confirmation-modal.html* Additionally, each item displays its category.

**admin_items()** same as *menu()* but we render *items.html*


### /admin-items/delete/<int:burger_id>
**admin_delete_item(burger_id)** expects a **burger_id** parameter from the URL and, upon receiving it, proceeds to delete the corresponding item in the menu table using the matching id.


### /admin-items/edit/<int:burger_id> and  /admin-items/add
Both routes work in similar ways, but have some small but important differences.

**/templates/admin/ edit-item.html** and  **add-item.html** both comprise of a form with a name, description, price, category and image URL field. When editing an item, the fields will be auto-filled with the information of the selected item. Conversely, when adding a new item, all fields will be left blank.

**admin_edit_item(burger_Id)** and **admin_add_item()** both use **add_edit_items()** to validate that non of the fields were left empty and to query for the *menu* table. They both pass categories as a parameter to their respective HTML file. The sole distinction arises when editing the item, requiring the burger_id to retrieve the corresponding information from the *menu* table and prepopulate the form.


### /admin-users
**/templates/admin/users.html** displays the list of all users that are admins, each with a ‘delete’ button, embedded with a from and the id of the user. Just as *order.html*, deleting an item will trigger *confirm-modal.html*. To prevent users from deleting themselves, their own account will be greyed out and disabled. Additionally, there's a form enabling administrators to add another admin by entering an email registered on the website.

**admin_users()** simply queries the *admins* table to pass it to *users.html* as a parameter



### /admin-users/delete/<int:admin_id>
**admin_users_delete(admin_id)** simply deletes the user from the *admins* if it matches **admin_id**. Once finished, it redirects the user to */admin-users*

### /admin-users/add
**admin_add_user()** It will utilize the email entered by the user in */admin-users* to check for matches in both the *users* table, verifying if it's a registered account on the website, and the *admins* table, to prevent the addition of an existing admin. Upon successful checks, the user's ID will be inserted into the *admins* table, and they will be redirected to */admin-users*.


## /project/static
In this route, will find one folder called *uploads* which contains the pages web icon, logo and promotional video seen in *index.html*. Additionally, there is a *style.css* file, encompassing all the styling for the web page and making use of media queries to adapt it for mobile devices. Finally, and most importantly, there are 8 javascript files integral to enhancing the functionality of the webpage and improving the overall user experience.


### toggleClass.js
**toggleIsValidClass(element, className)** is present in both *adminHandler.js* and *registerHandler.js*. This straightforward function facilitates the toggling of Bootstrap's valid and invalid classes for forms. It accepts two parameters: **element**, representing the HTML element for which the class needs modification, and **className**, determining whether the element should toggle to 'is-valid' or 'is-invalid'.

### adminHandler.js
**adminHandler.js** is used by two files; *edit-item.html* and *add-item.html*. Its primary function is to implement fundamental form validation and provide immediate feedback to users on the frontend. The file also contains a function **isImageUrl(url)**, created by [ChatGPT](https://openai.com/chatgpt),  which returns true if valid; otherwise, it will return false.

### alert.js
The file contains one function, **callAlert(type)**, used in *burger-detail.html* and *order.html*, which inserts a bootstrap alert on the top of the html file, to notify the user they cannot perform a certain action. The parameter **type** determines the message inside the alert.

### categoryHandler.js
The *categoryHandler.js* script, utilized in *menu.html* and *items.html*, dynamically filters items based on user-selected categories (Burgers, Sides, Beverages, Desserts). It employs an event listener on the "category-filter" element and a function, **displaySelectedItems(selectedCategory)**, to modify item visibility based on category attributes embedded in each of the items HTML data attributes.

### confirmDeleteHandler.js
The file contains **confirmDelete(id)**, prevents the deletion forms in *items.html* and *users.html*  from submitting and instead showing *confirm-modal.html*. Upon confirmation, the function utilizes the provided **id** to identify and submit the intended form. Its primary purpose is to safeguard administrators against accidental deletion of items or other administrators.

### formHandler.js
The file is used in  *login.html* and *checkout.html*, where it uses bootstrap to apply styling and some basic feedback when the form is incorrectly filled.

### orderHandler.js
The *orderHandler.js* file, utilized by *order.html*, encapsulates six distinct functions. The primary function, **updateOrder(event, orderId)**, dynamically manages the user's order quantity by either adding or subtracting items. The event parameter specifies whether to 'add' or 'subtract,' while **orderId** identifies the targeted item. Subsequently, four auxiliary functions are invoked: **toggleTrashIcon()** alters icons based on item quantities, **calculateTotal()** computes the total order price, **toggleClearOrderBtn()** manages the clear order button's visibility, and **updateUserOrder(orderId, newQuantity)** asynchronously updates the quantity in the database. If subtracting the amount results in zero, **deleteItem(orderId, newCartAmount)* is called, removing the HTML element and updating the backend accordingly.

The final function, **clearOrderModal()**, activates when the clear order button is confirmed (by *confirm-modal.html*), systematically removing all orders from the HTML.

Moreover, two event listeners enhance the script's functionality. The first, triggered on 'DOMContentLoaded,' ensures that upon page loading, essential values are updated by invoking **toggleTrashIcon()**, **calculateTotal()**, and **toggleClearOrderBtn()**. The second listener responds to the button click in the *confirm-modal.html* for clearing the order. This action sets the cart in the navbar to 0 and subsequently calls **clearOrderModal()**, **calculateTotal()**, **toggleClearOrderBtn()**, and **updateUserOrder()** with 'clear-order' as the orderId, prompting the deletion of all user orders in the backend.


### registerHandler.js
The *registerHandler.js* file parallels the functionality of *formHandler.js*, with a focus on additional validation requirements specific for user registration. The code ensures that the password is a minimum of 8 characters and that the password and confirm password fields match. Once these checks are successfully completed, the form undergoes submission. This script plays a crucial role in enhancing the registration process by incorporating specific validations to guarantee data integrity and an extra layer of security in the frontend.
