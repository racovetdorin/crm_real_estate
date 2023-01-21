from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.utils.translation import ugettext as _

from crm.views import ImagesUploadView
from properties.utils import UserCanCreateAgent, UserHasPermissions
from users.filters import UserFilter
from users.forms import UserForm, UserUpdateForm
from users.models import User, UserImage


class UserCreateView(LoginRequiredMixin, UserCanCreateAgent, CreateView):
    model = User
    form_class = UserForm

    def form_valid(self, form):
        user = form.save(commit=False)

        if self.request.POST['password1'] == self.request.POST['password2']:
            user.password = make_password(self.request.POST['password1'])
            user.save()

            return super().form_valid(form)

        form.add_error(None, _("Passwords don't match"))
        return render(self.request, 'users/add.html', {'form': form})


class UserUpdateView(UserHasPermissions, LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    context_object_name = 'agent'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'images': UserImage.objects.filter(user=self.get_object()).order_by('position').values(),
            'storage_url': settings.CDN_MEDIA_URL,
        })
        return context

    def form_valid(self, form):
        data = self.request.POST
        images = []
        deleted_images = []

        for key, value in data.items():
            if 'delete-img' in key:
                image = UserImage.objects.get(id=int(value))
                image.delete()
                deleted_images.append(int(value))
            elif 'position-img' in key:
                images.append(int(value))

        for deleted_image_id in deleted_images:
            images.remove(deleted_image_id)

        for position, image_id in enumerate(images):
            image = UserImage.objects.get(id=image_id)
            image.position = position
            image.save()

        return super().form_valid(form)


class UserListView(LoginRequiredMixin, ListView):
    model = User
    context_object_name = 'agents'

    def get_context_data(self, **kwargs):
        filter_form = UserFilter(self.request.GET, queryset=self.get_queryset())

        context = super().get_context_data(object_list=filter_form.qs, **kwargs)
        context.update({
            'filter': filter_form,
            'storage_url': settings.CDN_MEDIA_URL
        })

        return context


class UserImagesUploadView(ImagesUploadView):
    IMAGE_MODEL = UserImage
    OBJECT_MODEL = User
    STORAGE_LOCATION = settings.STORAGE_LOCATION
    OBJECT_TYPE_STRING = 'user'
