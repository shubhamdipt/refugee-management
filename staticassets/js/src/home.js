var loading = $("#loading");
var transfer_page = 1;
var transfer_table = $("#transfer-table");
var transfer_body = $("#transfer-tbody");
var transfer_form = $("#transfer-search-form");
var transfer_page_input = $("#transfer-page");

function get_transfers(check_form) {
    if (check_form) {
        formcheck(transfer_form);
    }
    var html = '';
    transfer_body.html('');
    loading.show();
    transfer_table.hide();
    $.get("/api/get-transfers", transfer_form.serialize()).done(function (data) {
        for (var i = 0; i < data.results.length ; i++) {
            html += (
                "<tr>" +
                "<td>" + data.results[i].start_time + "</td>" +
                "<td>" + data.results[i].route + "</td>" +
                "<td>" + data.results[i].refugee_seats + "</td>" +
                "<td><a href='/refugee/reserve-transfer/" + data.results[i].id + "' data-confirm='Are you sure you want to reserve?'>" +
                "<button class='btn btn-sm btn-outline-success'>Reserve</button></a></td></tr>"
            );
        }
        if (html === '') {
            html = "<tr><td colspan=3>No results found</td></tr>";
        }
        transfer_body.append(html);
        transfer_table.show();
        loading.hide();
    })
}
$(function (){
    get_transfers(false);
    $("#transfer-search-form").submit(function (e){
        e.preventDefault();
        get_transfers(true);
    })
})
