var loading = $("#loading");
var transfer_route_details_tbody = $("#transfer-route-details-tbody");
var seat_availability_tbody = $("#seat-availability-tbody");

function get_transfer_details(url, transfer_id) {
    var html = '';
    var seat_html = "";
    transfer_route_details_tbody.html(html);
    seat_availability_tbody.html(seat_html);
    $.get(url + transfer_id).done(function(data){
        console.log(data);
        for([key, val] of Object.entries(data.object)) {
            $("#" + key).html(clean_value(val));
        }
        for (var i = 0; i < data.details.length ; i++) {
            html += "<tr>" +
                "<td>" + (i+1) + "</td>" +
                "<td>" + data.details[i].departure_time + "</td>" +
                "<td>" + data.details[i].city + "</td>" +
                "<td>" + data.details[i].address + "</td>" +
                "</tr>";
        }
        for (var j = 0; j < data.seats_availability.length ; j++) {
            seat_html += "<tr>" +
                "<td>" + data.seats_availability[j][0] + " -> " + data.seats_availability[j][1] + "</td>" +
                "<td>" + data.seats_availability[j][2] + "</td>" +
                "</tr>";
        }
        transfer_route_details_tbody.append(html);
        seat_availability_tbody.append(seat_html);
        $('#transferDetailsModal').modal('show');
    })
}

$(document).on('click', '.transfer-details', function(e){
    e.preventDefault();
    get_transfer_details('/organization/api/get-transfer-details/', $(this).attr('data-transfer-id'));
});
$(document).on('click', '.organization-transfer-details', function(e){
    e.preventDefault();
    get_transfer_details('/organization/api/get-transfer-details/', $(this).attr('data-transfer-id'));
});
