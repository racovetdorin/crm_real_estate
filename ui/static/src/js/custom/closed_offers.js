$("#id_closed_offers").hide()

$("#closed_offers_toggle").click(function() {
    $("#id_closed_offers").toggle()

    if($("#closed_offers_toggle").hasClass('fa-angle-double-down')) {
    $("#closed_offers_toggle").removeClass('fa-angle-double-down')
    $("#closed_offers_toggle").addClass('fa-angle-double-up')
    }

    else {
        $("#closed_offers_toggle").removeClass('fa-angle-double-up')
        $("#closed_offers_toggle").addClass('fa-angle-double-down')
    }
});
