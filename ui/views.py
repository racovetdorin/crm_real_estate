import datetime

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render

from clients.models import Client
from demands.models import Demand
from offers.models import Offer
from properties.models import Property
from users.models import User
from activities.models import Activity


@login_required
def dashboard(request):
    today = datetime.date.today()
    this_week = datetime.date.today() - datetime.timedelta(days=7)
    last_week = datetime.date.today() - datetime.timedelta(days=14)
    this_month = datetime.date.today() - datetime.timedelta(days=30)
    last_month = datetime.date.today() - datetime.timedelta(days=60)

    active_agents_this_month = User.objects.filter(last_login__range=(this_month, today)).count()
    active_agents_last_month = User.objects.filter(last_login__range=(last_month, this_month)).count()

    active_offers_this_week = Offer.objects.filter(created_at__gte=this_week).count()
    active_offers_last_week = Offer.objects.filter(created_at__gte=last_week,
                                                   updated_at__lte=this_week).count()

    active_demands_this_week = Demand.objects.filter(created_at__gte=this_week).count()
    active_demands_last_week = Demand.objects.filter(created_at__gte=last_week,
                                                     updated_at__lte=this_week).count()

    new_clients_this_month = Client.objects.filter(created_at__gte=this_month).count()
    new_clients_last_month = Client.objects.filter(created_at__gte=last_month,
                                                   created_at__lte=this_month).count()

    number_of_total_activities_this_month = Activity.objects.filter(user=request.user,
                                                                    created_at__gte=this_month).count()
    number_of_total_activities_last_month = Activity.objects.filter(user=request.user, created_at__gte=last_month,
                                                                    created_at__lte=this_month).count()
    number_of_done_activities_this_month = Activity.objects.filter(user=request.user, created_at__gte=this_month,
                                                                   status=Activity.Status.DONE).count()
    number_of_to_do_activities_this_month = Activity.objects.filter(user=request.user, created_at__gte=this_month,
                                                                    status=Activity.Status.TO_DO).count()
    number_of_in_progress_activities_this_month = Activity.objects.filter(user=request.user, created_at__gte=this_month,
                                                                          status=Activity.Status.IN_PROGRESS).count()

    number_of_total_properties_this_month = Property.objects.filter(user=request.user,
                                                                    created_at__gte=this_month).count()
    number_of_total_properties_last_month = Property.objects.filter(user=request.user, created_at__gte=last_month,
                                                                    created_at__lte=this_month).count()

    number_of_total_offers_this_month = Offer.objects.filter(user=request.user, created_at__gte=this_month,
                                                             is_closed=False).count()
    number_of_total_offers_last_month = Offer.objects.filter(user=request.user, created_at__gte=last_month,
                                                             created_at__lte=this_month,
                                                             is_closed=False).count()


    number_of_total_transacted_offers_this_month = Offer.objects.filter(user=request.user, created_at__gte=this_month,
                                                                        status=settings.STATUS.TRANSACTED).count()
    number_of_total_active_offers_this_month = Offer.objects.filter(user=request.user, created_at__gte=this_month,
                                                                    status=settings.STATUS.ACTIVE).count()

    number_of_total_demands_this_month = Demand.objects.filter(user=request.user,
                                                               created_at__gte=this_month).count()
    number_of_total_demands_last_month = Demand.objects.filter(user=request.user, created_at__gte=last_month,
                                                               created_at__lte=this_month).count()

    offers_with_commision = Offer.objects.filter(user=request.user, created_at__gte=this_month, status=settings.STATUS.ACTIVE)

    def percentage(last, this):
        percent_difference = None
        if last == 0 or this == 0:
            return percent_difference

        percent_difference = 100 - ((this * 100) / last)

        if last == 1:
            percent_difference = this * 100

        return str(percent_difference).strip('-')

    agents_percent_difference = percentage(active_agents_last_month, active_agents_this_month)
    offers_percent_difference = percentage(active_offers_this_week, active_offers_last_week)
    demands_percent_difference = percentage(active_demands_last_week, active_demands_this_week)
    clients_percent_difference = percentage(new_clients_last_month, new_clients_this_month)
    activities_percent_diffrence = percentage(number_of_total_activities_last_month,
                                              number_of_total_activities_this_month)
    properties_percent_diffrence = percentage(number_of_total_properties_last_month,
                                              number_of_total_properties_this_month)
    offers_percent_difference_agent = percentage(number_of_total_offers_last_month, number_of_total_offers_this_month)
    demands_percent_difference_agent = percentage(number_of_total_demands_last_month, number_of_total_demands_this_month)
    current_month_user_commisions = [offer.commission for offer in offers_with_commision if offer.commission]
    sum_of_commissions = sum(current_month_user_commisions)

    context = {
        'active_agents_this_month': active_agents_this_month,
        'active_agents_last_month': active_agents_last_month,
        'agents_percent_difference': agents_percent_difference,
        'active_offers_this_week': active_offers_this_week,
        'active_offers_last_week': active_offers_last_week,
        'offers_percent_difference': offers_percent_difference,
        'active_demands_this_week': active_demands_this_week,
        'active_demands_last_week': active_demands_last_week,
        'demands_percent_difference': demands_percent_difference,
        'new_clients_this_month': new_clients_this_month,
        'new_clients_last_month': new_clients_last_month,
        'clients_percent_difference': clients_percent_difference,
        'total_clients': Client.objects.all().count(),
        'total_offers': Property.objects.select_related('offers').filter(offers__is_closed=False).annotate(
            total=Count('offers')).count(),
        'total_demands': Demand.objects.all().count(),
        'total_users': User.objects.filter(is_active=True).count(),
        'number_of_total_activities_this_month': number_of_total_activities_this_month,
        'number_of_done_activities_this_month': number_of_done_activities_this_month,
        'number_of_to_do_activities_this_month': number_of_to_do_activities_this_month,
        'number_of_in_progress_activities_this_month': number_of_in_progress_activities_this_month,
        'activities_percent_diffrence': activities_percent_diffrence,
        'number_of_total_properties_this_month': number_of_total_properties_this_month,
        'number_of_total_properties_last_month': number_of_total_properties_last_month,
        'properties_percent_diffrence': properties_percent_diffrence,
        'number_of_total_offers_this_month': number_of_total_offers_this_month,
        'number_of_total_offers_last_month': number_of_total_offers_last_month,
        'offers_percent_difference_agent': offers_percent_difference_agent,
        'number_of_total_transacted_offers_this_month': number_of_total_transacted_offers_this_month,
        'number_of_total_active_offers_this_month': number_of_total_active_offers_this_month,
        'number_of_total_demands_this_month': number_of_total_demands_this_month,
        'number_of_total_demands_last_month': number_of_total_demands_last_month,
        'demands_percent_difference_agent': demands_percent_difference_agent,
        'offers_with_commision' : offers_with_commision,
        'sum_of_commissions' : sum_of_commissions,

    }

    return render(request, 'users/dashboard.html', context)


@login_required()
def tutorials(request):
    context = {
        'crm_tutorials': settings.CRM_TUTORIALS
    }
    return render(request, 'users/tutorials.html', context)


@login_required
def offers_add(request):
    return render(request, 'offers/add.html')


@login_required
def offers(request):
    return render(request, 'offers/list.html')


@login_required
def contacts(request):
    return render(request, 'contacts/list.html')
