var stops_table=$("#stops-table"),transfer_form=$("#transferForm"),loading=$("#loading");function add_stops(){var r=stops_table.find("tr").length;$.get("/organization/api/get-pick-up-points").done(function(e){for(var t="<select class='autocomplete-stops' name='stopover-"+(r+1)+"' required>",s=0;s<e.results.length;s++){var a=e.results[s].address+", "+e.results[s].city+", "+e.results[s].country;t+="<option value='"+e.results[s].id+"'>"+a+"</option>"}stops_table.append("<tr><td style='width: 50px;'><div style='margin-top: 5px;'>#"+(r+1)+"</div></td><td>"+(t+="</select>")+'</td><td style="width: 130px;"><input class="form-control date-picker" name="date-'+(r+1)+'" value="" type="text" placeholder="Date" autocomplete="off" required></td><td style="width: 80px;"><input class="form-control time-picker" name="time-'+(r+1)+'" value="" type="text" placeholder="Time" autocomplete="off" required></td></tr>')}).always(function(){$(".autocomplete-stops").selectpicker(),$(".time-picker").datetimepicker({datepicker:!1,format:"H:i",step:5}),$(".date-picker").datetimepicker({timepicker:!1,format:"d/m/Y",formatDate:"Y/m/d"})})}function clearTransferForm(){stops_table.html(""),transfer_form.find("input, textarea, button").val("")}function submitTransfer(e){var s=$(this),a=$("#formResult"),r=s.find(".ajaxLoader");return a.css("display","none"),r.css("display","block"),e.preventDefault(),$.ajax({data:s.serialize(),type:"POST",url:s.attr("action"),success:function(e,t){r.css("display","none"),e.form&&(s.find(".formFields").html(e.form),a.css("display","none"),a.removeClass().addClass("formResult hidden"),alertMessage()),void 0!==e.success&&(a.removeClass().addClass("alert alert-success form-success"),a.fadeIn("slow"),alertMessage(),s.hasClass("onlyOnce")&&s.find("input, textarea, select, button").prop("disabled",!0)),void 0!==e.error&&(a.removeClass().addClass("alert alert-danger form-error"),a.fadeIn("slow"),alertMessage()),a.html(void 0===e.success?e.error:e.success),a.fadeIn("slow")},error:function(e,t){500===e.status&&(r.css("display","none"),a.removeClass().addClass("alert alert-danger form-error"),a.html("Unknown server error! Please contact support or try again later."),a.fadeIn("slow")),404!==e.status&&502!==e.status||(r.css("display","none"),a.removeClass().addClass("alert alert-danger form-error"),a.html("The server is currently unreachable. Please contact support or try again later."),a.fadeIn("slow")),a.html(t.message),a.fadeIn("slow")},complete:function(e,t){a.fadeIn("slow")}}),!1}$(function(){transfer_form.submit(submitTransfer)}),$("#add-stop").click(function(e){e.preventDefault(),add_stops()}),$("#reset").click(function(e){e.preventDefault(),stops_table.html("")});