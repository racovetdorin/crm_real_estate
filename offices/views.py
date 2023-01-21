from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView

from crm.views import ImagesUploadView
from offices.forms import OfficeForm
from offices.models import Office, OfficeImage


class OfficesListView(LoginRequiredMixin, ListView):
    model = Office

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'storage_url': settings.CDN_MEDIA_URL,
        })
        return context


class OfficeUpdateView(LoginRequiredMixin, UpdateView):
    model = Office
    form_class = OfficeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'images': OfficeImage.objects.filter(office=self.get_object()).order_by('position').values(),
            'storage_url': settings.CDN_MEDIA_URL,
        })
        return context

    def form_valid(self, form):
        counter = 0
        for k, v in self.request.POST.items():
            for image in OfficeImage.objects.filter(office_id=self.get_object()):
                if k.startswith('image'):
                    if str(image.id) == str(v):
                        image.position = counter
                        image.save()
                        counter += 1

                elif k.startswith('delete'):
                    if str(image.id) == str(v):
                        image.delete()

        return super().form_valid(form)


class OfficeImagesUploadView(LoginRequiredMixin, ImagesUploadView):
    IMAGE_MODEL = OfficeImage
    OBJECT_MODEL = Office
    STORAGE_LOCATION = settings.STORAGE_LOCATION
    OBJECT_TYPE_STRING = 'office'
