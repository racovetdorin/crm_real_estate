from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from locations.models import City, StreetNumber, Zone, Street


@login_required
def load_cities(request):
    region_id = request.GET.get('region')
    cities = City.objects.filter(region_id=region_id, id_999__isnull=False).order_by('name')

    return render(request, 'locations/partials/_city_dropdown_list_options.html', {'cities': cities})


@login_required
def load_zones(request):
    city_id = request.GET.get('city')
    zones = Zone.objects.filter(city_id=city_id, id_999__isnull=False).order_by('name')

    return render(request, 'locations/partials/_zone_dropdown_list_options.html', {'zones': zones})


@login_required
def load_streets(request):
    zone_id = [zone for zone in request.GET.getlist('zone') if zone]
    city_id = request.GET.get('city')

    streets = Street.objects.filter(city_id=city_id).order_by('id_999', 'name')

    if not request.GET.get('no-zone-filtering') == 'true':
        if zone_id:
            streets = streets.filter(zone_id__in=zone_id)

    return render(request, 'locations/partials/_street_dropdown_list_options.html', {'streets': streets})

@login_required
def load_street_numbers(request):
    street = request.GET.get('street')

    streets_numbers = StreetNumber.objects.filter(street__id=street)
    if len(streets_numbers) == 0:
        return HttpResponse('False')
    return render(request, 'locations/partials/_street_number_dropdown_list_options.html', {'streets_numbers': streets_numbers})

@login_required
def load_street_numbers_coordinates(request):
    street_number_name = request.GET.get('street_number_name')
    street_id = request.GET.get('street_id')
    print(type(street_number_name))

    coordinates = StreetNumber.objects.get(number=street_number_name, street__id=street_id)

    return JsonResponse({'latitude': coordinates.latitude, 'longitude': coordinates.longitude})
