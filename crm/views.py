import hashlib

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from properties.models import PropertyDocument
from storage import storage


def health(request):
    return HttpResponse("OK", status=200)


@method_decorator(csrf_exempt, name='dispatch')
class ImagesUploadView(View):
    class Meta:
        abstract = True

    IMAGE_MODEL = None
    OBJECT_MODEL = None
    STORAGE_LOCATION = None
    OBJECT_TYPE_STRING = None

    def post(self, request, pk):
        """
        The X-CSRFToken needs to be set in the request headers in order for this request to function over AJAX.
        """
        images = request.FILES.getlist('file')

        for image in images:
            # add form error
            if image.content_type not in ('image/jpeg',):
                continue

            location = '/'.join([self.STORAGE_LOCATION, self.OBJECT_TYPE_STRING, str(pk)])
            key = hashlib.md5(image.read()).hexdigest() + '.jpeg'
            image.seek(0)
            storage.save(image, location, key, public=True)

            image_path = "{}/{}".format(location, key)

            image_dict = {
                'image_path': image_path,
                'image_name': image.name,
                self.OBJECT_TYPE_STRING: get_object_or_404(self.OBJECT_MODEL, id=pk)
            }

            self.IMAGE_MODEL(**image_dict).save()

        return HttpResponse("OK")


class DocumentsUploadView(View):
    DOCUMENT_MODEL = None
    OBJECT_MODEL = None
    DOCUMENTS_STORAGE_LOCATION = None
    OBJECT_TYPE_STRING = None

    def post(self, request, pk):
        """
        The X-CSRFToken needs to be set in the request headers in order for this request to function over AJAX.
        """

        for key, value in self.request.POST.items():
            if 'delete-document' in key:
                image = PropertyDocument.objects.get(id=int(value))
                image.delete()

        documents = request.FILES.getlist('documents')

        for document in documents:
            # add form error
            location = '/'.join([self.DOCUMENTS_STORAGE_LOCATION, self.OBJECT_TYPE_STRING, str(pk)])
            key = hashlib.md5(document.read()).hexdigest() + '.' + document.name.split('.')[1]
            document.seek(0)
            storage.save(document, location, key, public=True)

            document_path = "{}/{}".format(location, key)

            document_dict = {
                'document_path': document_path,
                'document_name': document.name,
                self.OBJECT_TYPE_STRING: get_object_or_404(self.OBJECT_MODEL, id=pk)
            }

            self.DOCUMENT_MODEL(**document_dict).save()

        return redirect(request.POST.get('property_path'))


def bad_request(request, *args, **argv):
    response = render(request, '400.html', {})
    return response


def permission_denied(request, *args, **argv):
    response = render(request, '403.html', {})
    return response


def page_not_found(request, *args, **argv):
    response = render(request, '404.html', {})
    return response


def server_error(request, *args, **argv):
    response = render(request, '500.html', {})
    return response


def trigger_error(request):
    division_by_zero = 1 / 0
