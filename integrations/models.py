from django.db import models
from django.utils.translation import ugettext_lazy as _
# Create your models here.


class Integration(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Name"))
    api_key = models.CharField(max_length=100, blank=True, null=True,
                               verbose_name=_("API key"))
    secret_key = models.CharField(max_length=100, blank=True,
                                  null=True, verbose_name=_("Secret integration key"),
                                    )
    region_id = models.IntegerField(blank=True, null=True, verbose_name=_("Region ID"))
    integrator_id = models.IntegerField(blank=True, null=True, verbose_name=_("Integrator ID"))
    refresh_token = models.CharField(max_length=300, blank=True, null=True, verbose_name=_("Refresh token"))


    def __str__(self):
        return self.name
