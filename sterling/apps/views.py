# Create your views here.
from registration.backends.simple.views import RegistrationView

from django.views.generic import ListView
from django.core.urlresolvers import reverse

from .models import MobileApp

class AppListView(ListView):
    content_object_name = "app_list"
    template_name = "dashboard.html"

    def get_queryset(self):
        return MobileApp.objects.filter(users__exact=self.request.user)

class SterlingRegistrationView(RegistrationView):

    def get_success_url(self, request, user):
        return reverse("dashboard")


