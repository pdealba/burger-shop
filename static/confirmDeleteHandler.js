function confirmDelete(id) {
    // Triggers modal to open
    const confirmModal = document.getElementById('confirm-del-modal');
    let modal = new bootstrap.Modal(confirmModal);
    modal.show();

    // If the users clicks the confirm button the selected form is submitted
    // All forms have an id of form-delete-{{id}} with 'id' being the unique id of the item
    document.getElementById('confirm-button').addEventListener('click', function() {
        document.getElementById("form-delete-" + id).submit();
    });
}
