from django.contrib.auth.views import login, logout
from django.conf.urls import patterns, include, url
from splash.views import SplashFormView
from vanilla import RedirectView
from apps.views import AppListView, AppCreateView, AppDetailView, SterlingRegistrationView, \
AppDemographicsView, AppAlgorithmsView, AppSettingsView, AppHomeView, AppHelpView


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# TODO: Separate urls into different apps
urlpatterns = patterns('',
    # Examples:
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', SplashFormView.as_view(), name="index"),
    url(r'^login/$', login, {'template_name': 'login.html'}, name="login"),
    url(r'^logout/$', logout, {'next_page': '/'}, name="logout"),
    url(r'^apps/$', AppHomeView.as_view(), name="dashboard"),
    url(r'^apps/list/$', AppListView.as_view(), name='app_list'),
    url(r'^apps/detail/(?P<pk>\d+)/$', AppDetailView.as_view(), name="detail_app"),
    url(r'^apps/detail/(?P<pk>\d+)/demographics/$', AppDemographicsView.as_view(), name="demographics_app"),
    # url(r'^apps/detail/(?P<pk>\d+)/algorithms/$', AppAlgorithmsView.as_view(), name="algorithms_app"),
    url(r'^apps/detail/(?P<pk>\d+)/settings/$', AppSettingsView.as_view(), name="settings_app"),
    url(r'^help/$', AppHelpView.as_view(), name="help"),
    url(r'^apps/create/$', AppCreateView.as_view(), name="create_app"),
    url(r'^accounts/register/', SterlingRegistrationView.as_view(), name="registration_register"),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^', include('suggestions.urls')),
    url(r'^django-rq/', include('django_rq.urls')),
)
