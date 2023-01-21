function filter_ajax(element) {
    element.select2({
      ajax: {
        url: element.attr('data-search-url'),
        dataType: 'json',
        delay: 750,
        data: function (params) {
          console.log('reaches')
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

var offers_of_interest_el = $('#offers_of_interest-select')
var demands_of_interest_el = $('#demands_of_interest-select')

filter_ajax(offers_of_interest_el)
filter_ajax(demands_of_interest_el)
