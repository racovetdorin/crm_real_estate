import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status

from activities.models import Activity


@csrf_exempt
def change_status(request, activity_id):
    activity = Activity.objects.get(id=activity_id)

    activity_status = json.loads(request.body)['status']
    if activity_status not in Activity.Status:
        return JsonResponse("Not found", status=status.HTTP_404_NOT_FOUND, content_type='application/json', safe=False)

    activity.status = Activity.Status(activity_status)
    activity.save(update_fields=['status'])

    return JsonResponse("OK", status=status.HTTP_200_OK, content_type='application/json', safe=False)
