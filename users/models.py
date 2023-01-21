import json
import uuid

from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from eav.decorators import register_eav
from multiselectfield import MultiSelectField

from crm.models import ImageModel
from offices.models import Office


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    class LayoutSettings(models.TextChoices):
        DARK_MODE = 'darkMode', _('Dark mode')
        CONDENSED_SIDEBAR = 'leftSidebarCondensed', _('Condensed sidebar')
    
    Certificate_choices = (('power_start', 'Power Start'),
               ('juridic', 'Juridic'),
               ('succed', 'Succed'),
               ('next_level', 'Next level in Real Estate'),
               ('you_and_remax', 'Tu și REMAX'),
               ('executive', 'Executive'))

    username = None

    first_name = models.CharField(verbose_name=_('First name'), max_length=150, blank=True, default='')
    last_name = models.CharField(verbose_name=_('Last name'), max_length=150, blank=True, default='')
    email = models.EmailField('Email', unique=True)
    phone = models.CharField(max_length=20, null=True, verbose_name=_('Phone'))
    office = models.ForeignKey(Office, db_index=True, null=True, on_delete=models.SET_NULL, related_name='users',
                               verbose_name=_('Office'))
    role = models.CharField(max_length=256, blank=True, null=True, choices=settings.ROLES.choices, verbose_name=_('Role'))
    layout_settings = MultiSelectField(blank=True, null=True, choices=LayoutSettings.choices,
                                       verbose_name=_('Layout settings'))
    show_on_site = models.BooleanField(default=True)
    position_on_site = models.IntegerField(default=999999)
    objects = UserManager()
    display_title = models.CharField(verbose_name=_("Roles"), max_length=256, blank=True, default='')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    external_id = models.CharField(max_length=50, default=uuid.uuid4, 
                                   verbose_name=_('Agent external ID'))
    international_id = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('International ID'))
    agent_url = models.CharField(max_length=256, blank=True, null=True, verbose_name=_('Web Agent URL'))
    is_sale_associate = models.BooleanField(default=True, verbose_name=_('Is Sale associate'))
    promote_rex = models.BooleanField(default=True ,verbose_name=_('Promote Global'))
    specialization = models.PositiveIntegerField(default=1310, verbose_name=_('Specialization'))

    certificates = MultiSelectField(blank=True, null=True, choices=Certificate_choices,
                                       verbose_name=_('Certificates'))
    user_description = models.TextField(max_length=2000, blank=True, null=True, verbose_name=_('User Description'))
    token_999 = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('Token 999'))
    premium_999 = models.BooleanField(default=False ,verbose_name=_('Premium account 999'))


    class Meta:
        ordering = ['position_on_site', 'email']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def public_images(self):
        return self.images.filter(hide_on_site=False)

    @property
    def thumbnail(self):
        return self.images.filter(hide_on_site=False).first()

    @property
    def is_manager(self):
        manager_roles = [
            settings.ROLES.MANAGING_DIRECTOR,
            settings.ROLES.ASSISTANT_MANAGER,
            settings.ROLES.SECRETARIAT,
            settings.ROLES.BROKER_OWNER,
            settings.ROLES.OFFICE_MANAGER
        ]

        if (
                self.is_superuser
                or self.groups.filter(name__in=['Office Managers', 'Region Managers']).exists()
                or self.role in manager_roles
        ):
            return True

        return False

    def get_display_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_display_role(self):
        try:
            return settings.ROLES(self.role).label
        except ValueError:
            pass

    def get_display_full_name_phone(self):
        return '{} {} - ({})'.format(self.first_name, self.last_name, self.phone)

    def get_absolute_url(self):
        return reverse('ui:users_update', args=[self.pk])

    def get_display_object_class(self):
        return self.__class__.__name__

    def get_thumbnail_url(self):
        try:
            return self.images.filter(user_id=self.pk).first().image_path
        except AttributeError:
            return 'None'

    def get_full_thumbnail_url(self):
        if self.get_thumbnail_url():
            return settings.CDN_MEDIA_URL + self.get_thumbnail_url()

        return ''

    def get_layout_config(self):
        layout_config = {}
        for setting in self.layout_settings:
            layout_config[setting] = 'true'

        return json.dumps(layout_config)

    def can_view_client_details(self, client):
        if not client.is_private or self == client.user or self.is_manager:
            return True

        return False

    def can_edit_client(self, client):
        if not client.is_private or self == client.user or self.is_manager:
            return True

        return False

    def can_delete_client(self, client):
        if self.is_manager:
            return True

        return False

    def can_change_agent(self):
        if self.is_manager:
            return True

        return False


class UserImage(ImageModel):
    user = models.ForeignKey(User, related_name="images", on_delete=models.CASCADE,
                             verbose_name=_('User'), blank=True, null=True)

    def __str__(self):
        return 'Image for user with id: {}'.format(self.user.pk)


@register_eav()
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')


class Permissions(models.Model):
    class Meta:
        permissions = (
            ("can_view_administration_tab", "Can view administration tab"),
        )
