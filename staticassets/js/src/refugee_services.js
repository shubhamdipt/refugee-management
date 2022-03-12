var loading = $("#loading");
var transfer_page = 1;
var transfers_table = $("#transfers-table");
var transfers_tbody = $("#transfers-tbody");
var transfer_details_tbody = $("#transfer-details-tbody");

function get_transfers() {
    var html = '';
    transfers_tbody.html(html);
    loading.show();
    transfers_table.hide();
    $.get("/refugee/api/get-transfers").done(function (data) {
        for (var i = 0; i < data.results.length ; i++) {
            html += (
                "<tr>" +
                "<td>" + data.results[i].departure_time + "</td>" +
                "<td>" + data.results[i].seats + "</td>" +
                "<td><a href='#' class='reservation-details' data-reservation-id='" + data.results[i].id + "'>" + data.results[i].route + "</a></td>" +
                "<td><a class='delete-confirmation' href='/refugee/delete-transfer-reservation/" + data.results[i].id + "' data-confirm='Are you sure you want to delete?'>" +
                "<i class='fa fa-times-circle grey'></i></a></td></tr>"
            );
        }
        if (html === '') {
            html = "<tr><td colspan=4>No results found</td></tr>";
        }
        transfers_tbody.append(html);
        transfers_table.show();
        loading.hide();
    })
}
function get_transfer_reervation_details(reservation_id) {
    transfer_details_tbody.html('');
    var html = ''
    $.get('/refugee/api/get-transfer-reservation-details/' + reservation_id).done(function(data){
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
})
$(document).on('click', '.reservation-details', function(e){
    e.preventDefault();
    get_transfer_reervation_details($(this).attr('data-reservation-id'));
});
