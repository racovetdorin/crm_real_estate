$(".js-container-region-filter").change(function () {
  var url = $(".js-container-city-filter").attr("data-cities-url");  // get the url of the `load_cities` view
  var regionId = $('#region-select').children('option:selected').val();  // get the selected country ID from the HTML input

    $("#city-select").empty(); // empties the city field of any previous values
    $("#zone-select").empty(); // empties the zone field of any previous values
    $("#street-select").empty(); // empties the street field of any previous values

  $.ajax({                       // initialize an AJAX request
    url: url,                    // set the url of the request (= 0.0.0.0:8000/locations/cities/)
    data: {
      'region': regionId, // add the region id to the GET parameters
    },
    success: function (data) {   // `data` is the return of the `load_cities` view function
      $("#city-select").html(data);  // replace the contents of the city input with the data that came from the server
    }
  });

});


function populate_streets() {
  var url = $(".js-container-street-filter").attr("data-streets-url");  // get the url of the `load_streets` view
  var zoneIds = $("#zone-select :selected").map(function(i, el) {
        return parseInt($(el).val());
    }).get();
  var cityId = $('#city-select').children('option:selected').val();

  var data =  'city=' + cityId;
  $.each(zoneIds, function(key, value) {
      data += '&zone=' + value;
    });

  $("#street-select").empty(); // empties the street field of any previous values

  $.ajax({                       // initialize an AJAX request
    url: url,                    // set the url of the request (= 0.0.0.0:8000/locations/streets)
    data: data,
    success: function (data) {   // `data` is the return of the `load_streets` view function
      $("#street-select").html(data);  // replace the contents of the zone input with the data that came from the server
    }
  });
}

$(".js-container-city-filter").change(function () {
  var url = $(".js-container-zone-filter").attr("data-zones-url");  // get the url of the `load_zones` view
  var cityId = $('#city-select').children('option:selected').val();  // get the selected country ID from the HTML input

  $("#zone-select").empty(); // empties the zone field of any previous values

  $("#street-select").empty(); // empties the street field of any previous values

  $.ajax({                       // initialize an AJAX request
    url: url,                    // set the url of the request (= 0.0.0.0:8000/locations/zones)
    data: {
      'city': cityId       // add the city id to the GET parameters
    },
    success: function (data) {   // `data` is the return of the `load_zones` view function
      $("#zone-select").html(data);  // replace the contents of the zone input with the data that came from the server
      populate_streets()
    }
  });
});

$(".js-container-zone-filter").change(populate-streets);

