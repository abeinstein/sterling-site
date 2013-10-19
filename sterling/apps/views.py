# Create your views here.
from registration.backends.simple.views import RegistrationView
from vanilla import ListView, CreateView, DetailView

from django.core.urlresolvers import reverse, reverse_lazy

from .models import MobileApp, DevMembership

class AppListView(ListView):
    model = MobileApp
    template_name = "dashboard.html"

    def get_queryset(self):
        return MobileApp.objects.filter(users__exact=self.request.user)

class AppCreateView(CreateView):
    model = MobileApp
    success_url = reverse_lazy('dashboard')
    fields = ['facebook_id', 'name', 'invitation_message', 'link']

    def form_valid(self, form):
        form.instance.save()
        m = DevMembership(user=self.request.user,
                       mobile_app=form.instance,
                       is_admin=False)
        m.save()
        return super(AppCreateView, self).form_valid(form)

class AppDetailView(DetailView):
    model = MobileApp

    def get_context_data(self, **kwargs):
        context = super(AppDetailView, self).get_context_data(**kwargs)
        mobileapp = context['mobileapp']
        context['num_invited'] = mobileapp.num_invited()
        context['num_accepted'] = mobileapp.num_invitations_joined()
        if context['num_invited']:
            context['conversion_rate'] = float(context['num_accepted']) / context['num_invited']
        context['total_users'] = mobileapp.num_users()
        return context


class SterlingRegistrationView(RegistrationView):

    def get_success_url(self, request, user):
        return reverse("dashboard")


