$(".js-container-region").change(function () {
  var url = $(".js-container-city").attr("data-cities-url");  // get the url of the `load_cities` view
  var regionId = $('#region-select').children('option:selected').val();  // get the selected country ID from the HTML input
    $(".js-container-city").hide();
    $(".js-container-zone").hide();
    $(".js-container-street").hide();
    $(".js-container-contract").hide();

    $("#city-select").empty(); // empties the zone field of any previous values
    $("#zone-select").empty(); // empties the zone field of any previous values
    $("#street-select").empty(); // empties the street field of any previous values

  $.ajax({                       // initialize an AJAX request
    url: url,                    // set the url of the request (= 0.0.0.0:8000/locations/cities/)
    data: {
      'region': regionId, // add the region id to the GET parameters
    },
    success: function (data) {   // `data` is the return of the `load_cities` view function
      $("#city-select").html(data);  // replace the contents of the city input with the data that came from the server
      $(".js-container-city").show();
    }
  });

});


function populate_streets() {
  var url = $(".js-container-street").attr("data-streets-url");  // get the url of the `load_streets` view
  var zoneIds = $("#zone-select :selected").map(function(i, el) {
        return parseInt($(el).val()) || '';
    }).get();
  var cityId = $('#city-select').children('option:selected').val();

  var data =  'city=' + cityId;
  data += '&no-zone-filtering=' + $(".js-container-street").attr('data-no-zone-filtering')
  $.each(zoneIds, function(key, value) {
      data += '&zone=' + value;
    });

  // $("#street-select").empty(); // empties the street field of any previous values
  $(".js-container-contract").hide();
  $.ajax({                       // initialize an AJAX request
    url: url,                    // set the url of the request (= 0.0.0.0:8000/locations/streets)
    data: data,
    success: function (data) {   // `data` is the return of the `load_streets` view function
      $("#street-select").html(data);  // replace the contents of the zone input with the data that came from the server
      $(".js-container-street").show();
    }
  });
}

$(".js-container-city").change(function () {
  var url = $(".js-container-zone").attr("data-zones-url");  // get the url of the `load_zones` view
  var cityId = $('#city-select').children('option:selected').val();  // get the selected country ID from the HTML input

  $("#zone-select").empty(); // empties the zone field of any previous values
  $("#street-select").empty(); // empties the street field of any previous values

  $(".js-container-zone").hide();
  $(".js-container-street").hide();
  $(".js-container-contract").hide();

  $.ajax({                       // initialize an AJAX request
    url: url,                    // set the url of the request (= 0.0.0.0:8000/locations/zones)
    data: {
      'city': cityId       // add the city id to the GET parameters
    },
    success: function (data) {   // `data` is the return of the `load_zones` view function
      $("#zone-select").html(data);  // replace the contents of the zone input with the data that came from the server
      $(".js-container-zone").show();

      populate_streets()

      }
    });
});

// $(".js-container-zone").change(
//       !$(".js-container-street").attr('data-no-zone-filtering') ?
//       function () { populate_streets(); } :
//       null
// );

$(".js-container-street").change(function () {
    $(".js-container-contract").show();
    var street_id = $('#street-select').children('option:selected').val();
    if (street_id != ''){
    $.ajax({                       
      url: '/md/locations/street_numbers/',                    
      data: {
        'street': street_id, 
      },
      success: function (data) {  
        if(data != 'False'){
          var str_new_container = $('<div class="js-street-number-container form-group col-md-3" data-street-number="/md/locations/street_numbers/"><label>Număr stradă</label><select id="street-number-select" name="street_number" class="form-control select2" data-toggle="select2" required></select></div>');
          $('.street-number-container').replaceWith(str_new_container);
          $('#street-number-select').html(data);
        }
      }
    });
  }

});

$(document).on('change', '.js-street-number-container', function () {
      var street_number_name = $('#street-number-select').children('option:selected').val();
      var street = $('#street-select').children('option:selected').val();
      $.ajax({                       
        url: '/md/locations/street_numbers_coordinates/',                    
        data: {
          'street_number_name': street_number_name, 
          'street_id': street
        },
        success: function (data) {
          console.log(data)
          $("input[name='latitude']").val(data.latitude)
          $("input[name='longitude']").val(data.longitude)
        }
      });
    })


// window.location.reload(true)

$( document ).ready(function() {
  urlregion = $(".js-container-city").attr("data-cities-url"); 
  var regionId = $('#region-select').children('option:selected').val();
  var urlcity = $(".js-container-zone").attr("data-zones-url");  
  var cityId = $('#city-select').children('option:selected').val(); 
  var zoneId = $('#zone-select').children('option:selected').val();
  if (regionId != '' && cityId == ''){
    $.ajax({                       
          url: urlregion,                    
          data: {
            'region': regionId, 
          },
          success: function (data) {  
            $("#city-select").html(data); 
          }
        });
    }

    if (typeof(cityId) == 'string' && cityId.length > 0){
            $.ajax({                       
            url: urlregion,                    
            data: {
                'region': regionId, 
            },
            success: function (data) {  
                $("#city-select").html(data); 
                $("#city-select").val(cityId)
                // populate_streets();
            }
            });
        }
        
    

  if (cityId != '' && zoneId == ''){
    $.ajax({                      
        url: urlcity,                    
        data: {
        'city': cityId       
      },
      success: function (data) {   
        $("#zone-select").html(data); 
        // populate_streets();
        }
      });  
  }

  if (typeof(zoneId) == 'string' && zoneId.length > 0){
    $.ajax({                      
        url: urlcity,                    
        data: {
        'city': cityId       
    },
      success: function (data) {   
        $("#zone-select").html(data); 
        $("#zone-select").val(zoneId); 
        }
      });  
}


});