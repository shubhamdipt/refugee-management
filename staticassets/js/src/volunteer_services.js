var stops_table = $("#stops-table");
var transfer_form = $("#transferForm");
var loading = $("#loading");
var transfer_page = 1;
var transfers_table = $("#transfers-table");
var transfers_tbody = $("#transfers-tbody");
var transfer_details_tbody = $("#transfer-details-tbody");

function add_stops() {
    var stop_number = stops_table.find('tr').length;
    $.get("/locations/cities")
    .done(function (data){
        var html = "<select class='autocomplete-stops' name='city-" + (stop_number + 1) + "' required>";
        for (var i = 0; i < data.results.length ; i++) {
            html += "<option value='" + data.results[i].id + "'>" + data.results[i].text + "</option>"
        }
        html += "</select>";
        stops_table.append("<tr>" +
          "<td style='width: 50px;'><div style='margin-top: 5px;'>#" + (stop_number+1) + "</div></td>" +
          "<td>" + html + "</td>" +
          '<td><input class="form-control date-time-picker" name="datetime-' + (stop_number + 1) + '" value="" type="text" placeholder="Departure time" required></td>' +
          '<td><input class="form-control" name="address-' + (stop_number + 1) + '" value="" type="text" placeholder="Pick up address" autocomplete=off required></td>' +
          "</tr>");
    })
    .always(function () {
        $('.autocomplete-stops').selectpicker();
        $('.date-time-picker').datetimepicker({
            "allowInputToggle": true,
            "showClose": true,
            "showClear": true,
            "showTodayButton": true,
            "format": "DD/MM/YYYY HH:mm",
        });
    });
}
function clearTransferForm() {
    stops_table.html('');
    transfer_form.find('input, textarea, button').val('');
}
function get_transfers() {
    var html = '';
    transfers_tbody.html(html);
    loading.show();
    transfers_table.hide();
    $.get("/volunteer/api/get-transfers").done(function (data) {
        for (var i = 0; i < data.results.length ; i++) {
            html += (
                "<tr>" +
                "<td>" + data.results[i].start_time + "</td>" +
                "<td>" + data.results[i].seats + "</td>" +
                "<td><a href='#' class='transfer-details' data-transfer-id='" + data.results[i].id + "'>" + data.results[i].route + "</a></td>" +
                "<td>" + data.results[i].vehicle + "</td>" +
                "<td>" + data.results[i].vehicle_registration_number + "</td>" +
                "<td>" + (data.results[i].active ? "<i class='fa fa-check-circle green'>" : "<i class='fa fa-times-circle red'>") + "</td>" +
                "<td><a class='delete-confirmation' href='/volunteer/delete-transfer-service/" + data.results[i].id + "' data-confirm='Are you sure you want to delete?'>" +
                "<i class='fa fa-times-circle grey'></i></a></td></tr>"
            );
        }
        if (html === '') {
            html = "<tr><td colspan=5>No results found</td></tr>";
        }
        transfers_tbody.append(html);
        transfers_table.show();
        loading.hide();
    })
}
function submitTransfer(e) {

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
                clearTransferForm();
                get_transfers();
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

function get_transfer_details(transfer_id) {
    transfer_details_tbody.html('');
    var html = ''
    $.get('/volunteer/api/get-transfer-details/' + transfer_id).done(function(data){
        for (var i = 0; i < data.details.length ; i++) {
            html += "<tr>" +
                "<td>" + (i+1) + "</td>" +
                "<td>" + data.details[i].departure_date_string + "</td>" +
                "<td>" + data.details[i].city__name + "</td>" +
                "<td>" + data.details[i].address + "</td>" +
                "</tr>";
        }
        transfer_details_tbody.append(html);
        $('#transferDetailsModal').modal('show');
    })
}

$(function () {
    get_transfers();
    transfer_form.submit(submitTransfer);
})
$("#add-stop").click(function (e){
    e.preventDefault();
    add_stops();
})
$("#reset").click(function (e) {
    e.preventDefault();
    stops_table.html('');
})
$(document).on('click', '.transfer-details', function(e){
    e.preventDefault();
    get_transfer_details($(this).attr('data-transfer-id'));
});
