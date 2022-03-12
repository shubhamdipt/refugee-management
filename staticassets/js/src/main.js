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


function alertMessage() {
    window.setTimeout(function() {
        $(".alert").fadeOut('slow');
    }, 5000);
}

function disableForm(form_element) {
    var length = form_element.elements.length, i;
    for (i=0; i < length; i++) {
        form_element.elements[i].disabled = true;
    }
}

function formcheck(element) {
    var fields = element.find('select, textarea, input').serializeArray();
    $.each(fields, function (i, field) {
        if (!field.value) alert(field.title + ' is required');
    });
}

/* AJAX form submission */
function sendAjaxRequest(e) {

    var form = $(this);
    var result = $('#formResult');
    var loader = form.find('.ajaxLoader');

    result.css('display', 'none');
    loader.css('display', 'block');

    e.preventDefault();

    $.ajax({
        data: form.serialize(),
        type: 'POST',
        url: form.attr('action'),
        success: function (response, status) {

            loader.css('display', 'none');

            if (response.form) {
                form.find('.formFields').html(response.form);
                result.css('display', 'none');
                result.removeClass().addClass('formResult hidden');
                alertMessage();
            }

            if (response.success !== undefined) {
                result.removeClass().addClass('alert alert-success form-success');
                result.fadeIn("slow");
                alertMessage();
                if (form.hasClass("onlyOnce")) {
                    form.find('input, textarea, select, button').prop("disabled", true);
                }
            }

            if (response.error !== undefined) {
                result.removeClass().addClass('alert alert-danger form-error');
                result.fadeIn("slow");
                alertMessage();
            }

            result.html(response.success === undefined ? response.error : response.success);
            result.fadeIn("slow");
        },
        error: function (jqXHR, response) {
            if (jqXHR.status === 500) {
                loader.css('display', 'none');
                result.removeClass().addClass('alert alert-danger form-error');
                result.html('Unknown server error! Please contact support or try again later.');
                result.fadeIn("slow");
            }
            if (jqXHR.status === 404 || jqXHR.status === 502) {
                loader.css('display', 'none');
                result.removeClass().addClass('alert alert-danger form-error');
                result.html('The server is currently unreachable. Please contact support or try again later.');
                result.fadeIn("slow");
            }
            result.html(response.message);
            result.fadeIn("slow");
        },
        complete: function (status, response) {
            result.fadeIn("slow");
        }
    });
    return false;
}

$(function () {
    $('.ajaxForm').submit(sendAjaxRequest);
    $('.date-time-picker').datetimepicker({
          "allowInputToggle": true,
          "showClose": true,
          "showClear": true,
          "showTodayButton": true,
          "format": "DD/MM/YYYY HH:mm",
    });
    $('.date-picker').datepicker({format: "dd/mm/yyyy"});
    $('.select-autocomplete').selectpicker();
});
