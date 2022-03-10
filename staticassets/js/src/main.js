// Confirmation for delete links
$(function () {
    $(document).on('click', '.delete-confirmation', function (event) {
        event.preventDefault();
        var choice = confirm(this.getAttribute('data-confirm'));
        if (choice) {
            window.location.href = this.getAttribute('href');
        }
    });
});
