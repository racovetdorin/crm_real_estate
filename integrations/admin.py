from django.contrib import admin
from .models import Integration
from .publisher_remax_global import REXAgentsHandlerAPI, REXOfficesHandlerAPI, REXPropertiesHandlerAPI
from users.models import User
# Register your models here.





admin.site.register(Integration)

