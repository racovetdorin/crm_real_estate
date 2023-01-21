from django.urls import path

from activities import api as activity_api

urlpatterns = [
    path('activity/<int:activity_id>/status', activity_api.change_status, name='api_activity_status_change')
]
