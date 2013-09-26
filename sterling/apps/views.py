# Create your views here.
from registration.backends.simple.views import RegistrationView
from vanilla import ListView, CreateView

from django.core.urlresolvers import reverse, reverse_lazy

from .models import MobileApp, Membership

class AppListView(ListView):
    model = MobileApp
    template_name = "dashboard.html"


    def get_queryset(self):
        return MobileApp.objects.filter(users__exact=self.request.user)

class AppCreateView(CreateView):
    model = MobileApp
    success_url = reverse_lazy('dashboard')
    fields = ['facebook_id', 'name', 'invitation_message']

    def form_valid(self, form):
        form.instance.save()
        m = Membership(user=self.request.user,
                       mobile_app=form.instance,
                       is_admin=False)
        m.save()
        return super(AppCreateView, self).form_valid(form)


class SterlingRegistrationView(RegistrationView):

    def get_success_url(self, request, user):
        return reverse("dashboard")


