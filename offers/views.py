import csv
import datetime
import json
from demands.models import Demand
import rollbar

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DeleteView
from django.utils.translation import ugettext as _


from offers.filters import TransactedOffersFilter
from offers.models import Offer
from properties.templatetags.custom_tags import translate_bool


@method_decorator(csrf_exempt, name='dispatch')
def offer_view_count(request):
    if request.method == 'POST':
        try:
            offer_id = int(json.loads(request.body)["offer_id"])
        except Exception as e:
            rollbar.report_message(message="Can't process json", level='error')
            return HttpResponse("Can't process json", status=400)

        if offer_id:
            try:
                offer = Offer.objects.get(id=offer_id)
            except Offer.DoesNotExist as e:
                rollbar.report_message(message=str(e), level='error')
                return HttpResponse('Offer not found', status=404)
            else:
                offer.view_count += 1
                offer.save()

                return HttpResponse("Offer count +1!",status=200)

        return HttpResponse('Offer id not provided', status=400)

    return HttpResponse(status=400)





class TransactedOfferListView(LoginRequiredMixin, ListView):
    paginate_by = settings.DEFAULT_PAGINATION
    model = Offer
    transacted_statuses = settings.TRANSACTED_STATUSES

    status_choices = settings.TRANSACTED_STATUSES_CHOICES

    def get_queryset(self):
        return Offer.objects.filter(user=self.request.user, status__in=self.transacted_statuses).order_by(
            '-closing_date')

    def get_context_data(self, **kwargs):
        filter_form = TransactedOffersFilter(self.request.GET, queryset=self.get_queryset())
        context = super().get_context_data(object_list=filter_form.qs, **kwargs)
        context['filter'] = filter_form
        context['status_choices'] = self.status_choices

        return context


class AllTransactedOfferListView(TransactedOfferListView):
    def get_queryset(self):
        return Offer.objects.filter(status__in=self.transacted_statuses).order_by('-closing_date')


@login_required
def export_transactions(request):
    file_name = 'transactions.csv'
    transacted_offers = []
    for transacted_offer in TransactedOffersFilter(request.GET, queryset=Offer.objects.filter(
            status=settings.STATUS.TRANSACTED)).qs.values():
        offer_object = Offer.objects.get(id=transacted_offer['id'])
        transacted_offer['office_name'] = offer_object.office
        transacted_offer['type'] = offer_object.get_type_display()
        transacted_offer['exclusive'] = translate_bool(offer_object.exclusive)
        transacted_offer['user_email'] = offer_object.user.email
        transacted_offer['user_name'] = offer_object.user.get_display_full_name()
        transacted_offers.append(transacted_offer)

    with open(file_name, mode='w+', encoding='utf-8') as log_file:
        field_names = settings.TRANSACTED_OFFERS_LOG_FIELDS

        log_writer = csv.DictWriter(log_file, fieldnames=field_names.keys(), extrasaction='ignore')
        log_writer.writerow(field_names)
        for transacted_offer in transacted_offers:
            log_writer.writerow(transacted_offer)


    log_file = open(file_name, 'r', encoding="utf-8")
    response = HttpResponse(log_file, content_type='text/csv')

    return response


@login_required
def offer_validation(request, pk):
    if request.user.is_manager:
        offer = get_object_or_404(Offer, id=pk)
        offer.is_validated = True
        offer.validation_date = datetime.datetime.now()
        offer.status = settings.STATUS.ACTIVE
        offer.save()
    else:
        messages.add_message(request, messages.WARNING,
                             _("You don't have the necessary rights to validate an offer!"))

    return redirect(request.GET.get('property_path', f'{request.get_host()}/properties/{pk}'))


@login_required
def offer_invalidation(request, pk):
    if request.user.is_manager:
        offer = get_object_or_404(Offer, id=pk)
        offer.is_validated = False
        offer.validation_date = None
        offer.status = settings.STATUS.PENDING
        offer.save()
    else:
        messages.add_message(request, messages.WARNING,
                             _("You don't have the necessary rights to invalidate an offer!"))

    return redirect(request.GET.get('property_path', f'{request.get_host()}/properties/{pk}'))


class OfferDeleteView(LoginRequiredMixin, DeleteView):
    model = Offer
    success_message = _('Offer deleted!')

    def get_success_url(self):
        return reverse(settings.PROPERTIES_UPDATE_ROUTE, args=[self.get_object().property.id])
