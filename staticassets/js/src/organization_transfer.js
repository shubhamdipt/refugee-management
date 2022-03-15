var stops_table = $("#stops-table");
var transfer_form = $("#transferForm");
var loading = $("#loading");


function add_stops() {
    var stop_number = stops_table.find('tr').length;
    $.get("/organization/api/get-pick-up-points")
    .done(function (data){
        var html = "<select class='autocomplete-stops' name='stopover-" + (stop_number + 1) + "' required>";
        for (var i = 0; i < data.results.length ; i++) {
            var option_text = data.results[i].address + ", " + data.results[i].city + ", " + data.results[i].country;
            html += "<option value='" + data.results[i].id + "'>" + option_text + "</option>"
        }
        html += "</select>";
        stops_table.append("<tr>" +
          "<td style='width: 50px;'><div style='margin-top: 5px;'>#" + (stop_number+1) + "</div></td>" +
          "<td>" + html + "</td>" +
          '<td style="width: 130px;"><input class="form-control date-picker" name="date-' + (stop_number + 1) + '" value="" type="text" placeholder="Date" autocomplete="off" required></td>' +
          '<td style="width: 80px;"><input class="form-control time-picker" name="time-' + (stop_number + 1) + '" value="" type="text" placeholder="Time" autocomplete="off" required></td>' +
          "</tr>");
    })
    .always(function () {
        $('.autocomplete-stops').selectpicker();
        $('.time-picker').datetimepicker({
          datepicker:false,
          format:'H:i',
          step:5
        });
        $('.date-picker').datetimepicker({
            timepicker:false,
            format:'d/m/Y',
            formatDate:'Y/m/d',
        });
    });
}
function clearTransferForm() {
    stops_table.html('');
    transfer_form.find('input, textarea, button').val('');
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
                // clearTransferForm();
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
