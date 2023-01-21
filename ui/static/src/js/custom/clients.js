$('.js-search-clients-input').keyup(function(event) {
    if (event.keyCode === 13) {
        $(".js-search-clients").click();
    }
});


$(".js-search-clients").click(function () {
    $('.js-search-clients').removeClass('mdi-account-search');
    $('.js-search-clients').html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>').addClass('disabled');

    var url = $(".js-search-clients").attr("data-get-form-url");
    var phoneNumber = $('.js-search-clients-input').val();
    $.ajax({
    url: url,
    data: {
      'phone': phoneNumber
    },
    success: function (data) {
      $("#js-clients-container-id").html(data);
      $(".js-search-clients").html('');
      $(".js-search-clients").addClass('mdi-account-search');
    }
    });

});
