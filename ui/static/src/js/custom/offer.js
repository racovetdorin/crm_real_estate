$(".js-offer-checkbox").click(function(event) {
    var divId = $(this).attr("data-container-id");
    var fieldsetId = $(this).attr("data-fieldset-id");

    if (event.target.checked) {
        $('#'+divId).show();
        $('#'+divId).children('fieldset')[0].disabled = false;
    } else {
        $('#'+divId).hide();
        $('#'+divId).children('fieldset')[0].disabled = true;
    }
});

$("#js-delete-all").click(function(event) {

  var checked = this.checked;
    $('.js-delete-checkbox').each(function() {
      this.checked = checked;
    });
});
