var loading=$("#loading"),transfer_details_tbody=$("#transfer-details-tbody"),transfer_route_details_tbody=$("#transfer-route-details-tbody");function clean_key(t){return t.replace("_"," ").replace(/(^|\s)\S/g,function(t){return t.toUpperCase()})}function clean_value(t){return null===t?"":t}function get_transfer_details(t,e){transfer_details_tbody.html(""),transfer_route_details_tbody.html("");var a="",r="";$.get(t+e).done(function(t){for([key,val]of Object.entries(t.object))r+="<tr><td>"+clean_key(key)+"</td><td>"+clean_value(val)+"</td></tr>";for(var e=0;e<t.details.length;e++)a+="<tr><td>"+(e+1)+"</td><td>"+t.details[e].departure_time+"</td><td>"+t.details[e].city+"</td><td>"+t.details[e].address+"</td></tr>";transfer_route_details_tbody.append(a),transfer_details_tbody.append(r),$("#transferDetailsModal").modal("show")})}$(document).on("click",".transfer-details",function(t){t.preventDefault(),get_transfer_details("/organization/api/get-transfer-details/",$(this).attr("data-transfer-id"))}),$(document).on("click",".organization-transfer-details",function(t){t.preventDefault(),get_transfer_details("/organization/api/get-organization-transfer-details/",$(this).attr("data-transfer-id"))});