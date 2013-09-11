from django.contrib.auth.views import login, logout
from django.conf.urls import patterns, include, url
from splash.views import SplashFormView
from apps.views import AppListView, SterlingRegistrationView


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', SplashFormView.as_view(), name="index"),
    url(r'^login/$', login, {'template_name': 'login.html'}, name="login"),
    url(r'^logout/$', logout, {'template_name': 'logout.html'}, name="logout"),
    url(r'^apps/$', AppListView.as_view(), name="dashboard"),
    url(r'^accounts/register/', SterlingRegistrationView.as_view(), name="registration_register"),
    url(r'^accounts/', include('registration.backends.simple.urls')),

    url(r'^', include('fbNodes.urls')),
)
