from django.contrib.auth import views as auth_views
from django.urls import include, path, reverse_lazy
from django.utils.translation import ugettext_lazy as _
from locations.api import RegionsListAPIView, CitiesListAPIView, ZonesListAPIView, StreetsListAPIView
from offers.api import ExclusiveOffersListAPIView, HomepageOffersListAPIView, OffersDetailsAPIView, OffersListAPIView, \
    ReservedOffersListAPIView, TransectedOffersListAPIView, SpecialOffersListAPIView, RecommendedOffersListAPIView
from clients import views as clients_views
from demands import views as demands_views
from locations import views as locations_views
from offers import views as offers_views
from offices.api import OfficesListAPIView
from properties import views as properties_views, utils
from activities import views as activities_views
from properties.api import FeaturesListAPIView
from users import views as users_views
from offices import views as office_views
from audit import views as audit_views
from ui import views
from users.api import UsersListAPIView

app_name = 'ui'

urlpatterns = [
     path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='crm_login'),
     path('logout/', auth_views.LogoutView.as_view(), name='crm_logout'),
     path('', views.dashboard, name='dashboard'),
     path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='crm_login'),
     path('logout/', auth_views.LogoutView.as_view(), name='crm_logout'),

     path('password_change/', auth_views.PasswordChangeView.as_view(template_name='users/password_change_form.html'),
          name='password_change/'),
     path('password_change/done/',
          auth_views.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'),
          name='password_change_done'),

     path('password_reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset_form.html',
                                                                      email_template_name='users/password_reset_email.html',
                                                                      success_url=reverse_lazy(
                                                                      'ui:password_reset_complete')),
          name='password_reset'),

     path('password_reset/done/',
          auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
          name='password_reset_done'),

     path('reset/<uidb64>/<token>/',
          auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html',
                                                       success_url=reverse_lazy('ui:password_reset_done')),
          name='password_reset_confirm'),
     path('reset/done/',
          auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
          name='password_reset_complete'),

     path('properties/add/', properties_views.PropertyCreateView.as_view(
          template_name="properties/add.html"
     ), name='property_create'),
     path('properties/<int:pk>/', properties_views.PropertyUpdateView.as_view(
          template_name="properties/update.html"
     ), name='property_update'),
     path('properties/<int:pk>/generate_record', properties_views.PropertyGenerateRecordView.as_view(
          template_name="properties/generate_record.html"
     ), name='property_generate_record'),

     path('properties/all/', properties_views.AllPropertiesListView.as_view(
          template_name="properties/list.html"
     ), name='all_properties_list'),
     path('properties/', properties_views.MyPropertiesListView.as_view(
          template_name="properties/list.html"
     ), name='my_properties_list'),
     path('properties/office/', properties_views.OfficePropertiesListView.as_view(
          template_name="properties/list.html"
     ), name='office_properties_list'),
     path('properties/delete/<int:pk>/', properties_views.PropertySoftDeleteView.as_view(
          template_name="properties/delete.html"
     ), name='property_delete'),
     path('properties/upload_images/<int:pk>/', properties_views.PropertyImagesUploadView.as_view(),
          name='property_upload_images'),
     path('properties/upload_documents/<int:pk>/', properties_views.PropertyDocumentsUploadView.as_view(),
          name='property_upload_documents'),
     path('properties/search/', properties_views.get_properties_by_query,
          name='ajax_search_properties'),
     path('properties/search/', properties_views.get_properties_by_offer_id_query,
          name='ajax_search_properties_by_offer_id'),



     path('clients/add/', clients_views.ClientCreateView.as_view(
          template_name="clients/update.html",
     ), name='client_create'),
     path('clients/<int:pk>/', clients_views.ClientUpdateView.as_view(
          template_name="clients/update.html"
     ), name='client_update'),
     path('clients/all/', clients_views.AllClientsListView.as_view(
          template_name="clients/list.html"
     ), name='all_clients_list'),
     path('clients/', clients_views.MyClientsListView.as_view(
          template_name="clients/list.html"
     ), name='my_clients_list'),
     path('clients/office/', clients_views.OfficeClientsListView.as_view(
          template_name="clients/list.html"
     ), name='office_clients_list'),
     path('clients/delete/<int:pk>/', clients_views.ClientSoftDeleteView.as_view(
          template_name="clients/list.html"
     ), name='client_delete'),

     path('demands/add/', demands_views.DemandCreateView.as_view(
          template_name="demands/update.html",
     ), name='demand_create'),
     path('demands/<int:pk>/', demands_views.DemandUpdateView.as_view(
          template_name="demands/update.html",
     ), name='demand_update'),
     path('demands/all/', demands_views.AllDemandListView.as_view(
          template_name="demands/list.html"
     ), name='all_demands_list'),
     path('demands/office/', demands_views.OfficeDemandsListView.as_view(
          template_name="demands/list.html"
     ), name='office_demands_list'),
     path('demands/', demands_views.MyDemandsListView.as_view(
          template_name="demands/list.html"
     ), name='my_demands_list'),
     path('demands/delete/<int:pk>/', demands_views.DemandSoftDeleteView.as_view(
          template_name="demands/list.html"
     ), name='demand_delete'),
     path('transacted-demands',
          demands_views.TransactedDemandsListView.as_view(template_name='demands/partials/list_transacted.html'),
          name='my_transacted_demands_list'),
     path('transacted-demands/all',
          demands_views.AllTransactedDemandsListView.as_view(template_name='demands/partials/list_transacted.html'),
          name='all_transacted_demands_list'),
     path('demands/search/', demands_views.get_demands_by_query,
          name='ajax_search_demands'),

     path('offers/view_count', offers_views.offer_view_count,
          name='view_count'),
     path('offers/delete/<int:pk>', offers_views.OfferDeleteView.as_view(),
          name='offer_delete'),
     path('transacted-offers',
          offers_views.TransactedOfferListView.as_view(template_name='offers/partials/list.html'),
          name='my_transacted_offers_list'),
     path('transacted-offers/all',
          offers_views.AllTransactedOfferListView.as_view(template_name='offers/partials/list.html'),
          name='all_transacted_offers_list'),
     path('transacted_offers/log/', offers_views.export_transactions,
          name='transacted_offers_log'),
     path('offers/validation/<int:pk>/', offers_views.offer_validation,
          name='offer_validation'),
     path('offers/invalidation/<int:pk>/', offers_views.offer_invalidation,
          name='offer_invalidation'),

     path('activities/create', activities_views.activity_create,
          name='activity_create'),
     path('activities/all', activities_views.AllActivitiesListView.as_view(
          template_name='activities/list.html'),
          name='all_activities_list'),
     path('activities/', activities_views.MyActivitiesListView.as_view(
          template_name='activities/list.html'),
          name='my_activities_list'),
     path('archived_activities/', activities_views.ArchivedActivitiesListView.as_view(
          template_name='activities/archived_activities_list.html'),
          name='archived_activities_list'),
     path('leads/', activities_views.MyLeadsListView.as_view(
          template_name='activities/list.html'),
          name='my_leads_list'),
     path('all_leads/', activities_views.AllLeadsListView.as_view(
          template_name='activities/list.html'),
          name='all_leads_list'),
     path('archived_leads/', activities_views.ArchivedLeadsListView.as_view(
          template_name='activities/archived_activities_list.html'),
          name='archived_leads_list'),
     path('archive_activities', activities_views.archive_activities, name='archive_activities'),

     path('users/add/', users_views.UserCreateView.as_view(
          template_name='users/add.html'),
          name='user_create'),
     path('users/list/', users_views.UserListView.as_view(
          template_name='users/list.html'),
          name='users_list'),
     path('users/<int:pk>', users_views.UserUpdateView.as_view(
          template_name='users/add.html'),
          name='users_update'),
     path('users/upload/<int:pk>/', users_views.UserImagesUploadView.as_view(),
          name='users_upload_images'),
     path('users/password_change', auth_views.PasswordChangeView.as_view(
          template_name='users/password_change_form.html',
          success_url=reverse_lazy('ui:password_change_done')),
          name='password_change'),
     path('users/password_change_done', auth_views.PasswordChangeDoneView.as_view(
          template_name='users/password_change_done.html'),
          name='password_change_done'),

     path('offices/list', office_views.OfficesListView.as_view(
          template_name='offices/list.html'),
          name='offices_list'),
     path('offices/<int:pk>', office_views.OfficeUpdateView.as_view(
          template_name='offices/update.html'),
          name='office_update'),
     path('offices/upload/<int:pk>/', office_views.OfficeImagesUploadView.as_view(),
          name='offices_upload_images'),

     path('audit/list', audit_views.AuditLogListView.as_view(
          template_name='audit/list.html'
     ), name='audit_list'),

     path('locations/cities/', locations_views.load_cities,
          name='ajax_load_cities'),
     path('locations/zones/', locations_views.load_zones,
          name='ajax_load_zones'),
     path('locations/streets/', locations_views.load_streets,
          name='ajax_load_streets'),
     path('locations/street_numbers/', locations_views.load_street_numbers,
          name='ajax_load_street_numbers'),
     path('locations/street_numbers_coordinates/', locations_views.load_street_numbers_coordinates,
          name='ajax_load_street_numbers_coordinates'),

     path('clients/hidden_client_create/', utils.client_form_handling,
          name='hidden_client_create'),
     path('clients/phone/', clients_views.get_clients_by_phone,
          name='ajax_load_clients_by_phone'),
     path('clients/search/', clients_views.get_clients_by_query,
          name='ajax_search_clients'),

     path('tutorials', views.tutorials, name='tutorials'),

     path('api/offers/list', OffersListAPIView.as_view(), name='offers_list_api'),
     path('api/offers/details/<int:pk>/', OffersDetailsAPIView.as_view(), name='offers_details_api'),
     path('api/regions/', RegionsListAPIView.as_view(), name='regions_list_api'),
     path('api/cities/', CitiesListAPIView.as_view(), name='cities_list_api'),
     path('api/zones/', ZonesListAPIView.as_view(), name='zones_list_api'),
     path('api/streets/', StreetsListAPIView.as_view(), name='streets_list_api'),
     path('api/exclusive_offers/', ExclusiveOffersListAPIView.as_view(), name='exclusive_offers_list_api'),
     path('api/recommended_offers/', RecommendedOffersListAPIView.as_view(), name='recommended_offers_list_api'),
     path('api/homepage_offers/', HomepageOffersListAPIView.as_view(), name='homepage_offers_list_api'),
     path('api/special_offers/', SpecialOffersListAPIView.as_view(), name='special_offers_list_api'),
     path('api/features/', FeaturesListAPIView.as_view(), name='features_list_api'),
     path('api/offices/', OfficesListAPIView.as_view(), name='features_list_api'),
     path('api/users/', UsersListAPIView.as_view(), name='features_list_api'),
     path('api/transacted/', TransectedOffersListAPIView.as_view(), name='transected_offers_list_api'),
     path('api/reserved/', ReservedOffersListAPIView.as_view(), name='reserved_offers_list_api'),
     path('django-rq/', include('django_rq.urls'))
]
