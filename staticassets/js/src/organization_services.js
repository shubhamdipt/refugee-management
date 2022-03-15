var loading = $("#loading");
var transfer_details_tbody = $("#transfer-details-tbody");
var transfer_route_details_tbody = $("#transfer-route-details-tbody");

function clean_key(text) {
    return text.replace('_', ' ').replace(/(^|\s)\S/g, function(t) { return t.toUpperCase() });
}
function clean_value(text) {
    return text === null ? "" : text;
}
function get_transfer_details(url, transfer_id) {
    transfer_details_tbody.html('');
    transfer_route_details_tbody.html('');
    var html = ''
    var details_html = ''
    $.get(url + transfer_id).done(function(data){
        for([key, val] of Object.entries(data.object)) {
            details_html += "<tr>" +
                "<td>" + clean_key(key) + "</td>" +
                "<td>" + clean_value(val) + "</td>" +
                "</tr>";
        }
        for (var i = 0; i < data.details.length ; i++) {
            html += "<tr>" +
                "<td>" + (i+1) + "</td>" +
                "<td>" + data.details[i].departure_time + "</td>" +
                "<td>" + data.details[i].city + "</td>" +
                "<td>" + data.details[i].address + "</td>" +
                "</tr>";
        }
        transfer_route_details_tbody.append(html);
        transfer_details_tbody.append(details_html);
        $('#transferDetailsModal').modal('show');
    })
}

$(document).on('click', '.transfer-details', function(e){
    e.preventDefault();
    get_transfer_details('/organization/api/get-transfer-details/', $(this).attr('data-transfer-id'));
});
$(document).on('click', '.organization-transfer-details', function(e){
    e.preventDefault();
    get_transfer_details('/organization/api/get-organization-transfer-details/', $(this).attr('data-transfer-id'));
});
