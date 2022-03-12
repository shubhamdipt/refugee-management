var stops_table=$("#stops-table"),transfer_form=$("#transferForm"),loading=$("#loading"),transfer_page=1,transfers_table=$("#transfers-table"),transfers_tbody=$("#transfers-tbody"),transfer_details_tbody=$("#transfer-details-tbody");function add_stops(){var r=stops_table.find("tr").length;$.get("/locations/cities").done(function(e){for(var t="<select class='autocomplete-stops' name='city-"+(r+1)+"' required>",s=0;s<e.results.length;s++)t+="<option value='"+e.results[s].id+"'>"+e.results[s].text+"</option>";stops_table.append("<tr><td style='width: 50px;'><div style='margin-top: 5px;'>#"+(r+1)+"</div></td><td>"+(t+="</select>")+'</td><td><input class="form-control date-time-picker" name="datetime-'+(r+1)+'" value="" type="text" placeholder="Departure time" required></td><td><input class="form-control" name="address-'+(r+1)+'" value="" type="text" placeholder="Pick up address" autocomplete=off required></td></tr>')}).always(function(){$(".autocomplete-stops").selectpicker(),$(".date-time-picker").datetimepicker({allowInputToggle:!0,showClose:!0,showClear:!0,showTodayButton:!0,format:"DD/MM/YYYY HH:mm"})})}function clearTransferForm(){stops_table.html(""),transfer_form.find("input, textarea, button").val("")}function get_transfers(){var s="";transfers_tbody.html(s),loading.show(),transfers_table.hide(),$.get("/volunteer/api/get-transfers").done(function(e){for(var t=0;t<e.results.length;t++)s+="<tr><td>"+e.results[t].start_time+"</td><td>"+e.results[t].seats+"</td><td><a href='#' class='transfer-details' data-transfer-id='"+e.results[t].id+"'>"+e.results[t].route+"</a></td><td>"+e.results[t].vehicle+"</td><td>"+e.results[t].vehicle_registration_number+"</td><td>"+(e.results[t].active?"<i class='fa fa-check-circle green'>":"<i class='fa fa-times-circle red'>")+"</td><td><a class='delete-confirmation' href='/volunteer/delete-transfer-service/"+e.results[t].id+"' data-confirm='Are you sure you want to delete?'><i class='fa fa-times-circle grey'></i></a></td></tr>";""===s&&(s="<tr><td colspan=5>No results found</td></tr>"),transfers_tbody.append(s),transfers_table.show(),loading.hide()})}function submitTransfer(e){var s=$(this),r=$("#formResult"),a=s.find(".ajaxLoader");return r.css("display","none"),a.css("display","block"),e.preventDefault(),$.ajax({data:s.serialize(),type:"POST",url:s.attr("action"),success:function(e,t){a.css("display","none"),e.form&&(s.find(".formFields").html(e.form),r.css("display","none"),r.removeClass().addClass("formResult hidden"),alertMessage()),void 0!==e.success&&(r.removeClass().addClass("alert alert-success form-success"),r.fadeIn("slow"),alertMessage(),s.hasClass("onlyOnce")&&s.find("input, textarea, select, button").prop("disabled",!0),clearTransferForm(),get_transfers()),void 0!==e.error&&(r.removeClass().addClass("alert alert-danger form-error"),r.fadeIn("slow"),alertMessage()),r.html(void 0===e.success?e.error:e.success),r.fadeIn("slow")},error:function(e,t){500===e.status&&(a.css("display","none"),r.removeClass().addClass("alert alert-danger form-error"),r.html("Unknown server error! Please contact support or try again later."),r.fadeIn("slow")),404!==e.status&&502!==e.status||(a.css("display","none"),r.removeClass().addClass("alert alert-danger form-error"),r.html("The server is currently unreachable. Please contact support or try again later."),r.fadeIn("slow")),r.html(t.message),r.fadeIn("slow")},complete:function(e,t){r.fadeIn("slow")}}),!1}function get_transfer_details(e){transfer_details_tbody.html("");var s="";$.get("/volunteer/api/get-transfer-details/"+e).done(function(e){for(var t=0;t<e.details.length;t++)s+="<tr><td>"+(t+1)+"</td><td>"+e.details[t].departure_date_string+"</td><td>"+e.details[t].city__name+"</td><td>"+e.details[t].address+"</td></tr>";transfer_details_tbody.append(s),$("#transferDetailsModal").modal("show")})}$(function(){get_transfers(),transfer_form.submit(submitTransfer)}),$("#add-stop").click(function(e){e.preventDefault(),add_stops()}),$("#reset").click(function(e){e.preventDefault(),stops_table.html("")}),$(document).on("click",".transfer-details",function(e){e.preventDefault(),get_transfer_details($(this).attr("data-transfer-id"))});