function filter_ajax(element) {
    element.select2({
      ajax: {
        url: element.attr('data-search-url'),
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

var activities_list = $('#js-activities-list')
var ids_string = activities_list.attr('data-activities-ids')
ids_string = ids_string.split('&')

ids_string.forEach(function(activity) {
    activitySplit = activity.split('-')
    activity_id = activitySplit[0]
    activity_fk_object = activitySplit[1]
    fk_obj_id = activitySplit[2]

    if(activity_fk_object === 'property') {
        propertyFkEl = $('#activity-' + activity_id + '-property-' + fk_obj_id)
        filter_ajax(propertyFkEl)
    }

    if(activity_fk_object === 'client') {
        clientFkEl = $('#activity-' + activity_id + '-client-' + fk_obj_id)
        filter_ajax(clientFkEl)
    }

    if(activity_fk_object === 'demand') {
        demandFkEl = $('#activity-' + activity_id + '-demand-' + fk_obj_id)
        filter_ajax(demandFkEl)
    }
})

var fk_array = ['activity_property_fk', 'activity_client_fk', 'activity_demand_fk','activity_property_fk_leads', 'activity_client_fk_leads', 'activity_demand_fk_leads', 'id-client-filter-select', 'id-property-filter-select']

fk_array.forEach(function(id) {
    fkElement = $('#'+id)
    filter_ajax(fkElement)
})
