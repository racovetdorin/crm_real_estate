// jQuery code for pre-adding csrf_token to ajax request
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$.ajaxPrefilter(function(options, originalOptions, jqXHR){
    if (options['type'].toLowerCase() === "post") {
        jqXHR.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
    }
});
// end


$("#id-form-client").hide();

$("#id-form-client-add-trigger").click(function () {
    $("#id-form-client").show();
});

$("#id-form-client").submit(function () {
    event.preventDefault();
    var url = $("#id-form-client-add").attr('action')
    console.log(url)

    $.ajax({
        url: url,
        type: 'post',
        data:$("#id-form-client-add").serialize(),
        success: function(data) {
            if (data !== null) {
                $('#id-client-select').html('<option selected value="'+data['last_client'][0]+'">'+data['last_client'][1]+'</option>')
            }
            $("#id-form-client").hide();
            $("#id-form-client-error-container").hide();
            $('#id-form-client-error-data').html('')
            window.location.href='#top';
        },
        error: function(data) {
            console.log(data.responseJSON)
            $("#id-form-client-error-container").show();
            $('#id-form-client-error-data').html('')
            for (var key in data.responseJSON) {
                if (data.responseJSON.hasOwnProperty(key)) {
                    $('#id-form-client-error-data').append('<strong>Error - </strong>' + data.responseJSON[key])
                }
            }
        }
    });
});

$("#id-close").click(function () {
    $("#id-form-client").hide();
})

var select2Els = [$('#id-client-select'), $('#id-offer-client-select'), $('#id-client-filter-select')];

for(var i=0; i < select2Els.length; i++) {
    console.log(select2Els[i].attr("data-search-url"))
    select2Els[i].select2({
      ajax: {
        url: select2Els[i].attr("data-search-url"),
        dataType: 'json',
        delay: 750,
        data: function (params) {
          console.log(params)
          return {
            'query': params.term
          }
        },
        processResults: function (data) {
           return {
            results: data.items
          };
        },
      }
    });
}
