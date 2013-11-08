# Create your views here.
from registration.backends.simple.views import RegistrationView
from vanilla import ListView, CreateView, DetailView, RedirectView
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect

from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import redirect

from .models import MobileApp, DevMembership

class AppHomeView(RedirectView):
    template_name = 'apps/mobileapp_detail.html'
    model = MobileApp

    def get_queryset(self):
        return MobileApp.objects.filter(users__exact=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        if self.get_queryset():
            return redirect('detail/%d' % int(self.get_queryset()[0].pk) )
        else:
            return redirect('list/')

#     def get_redirect_url(self, **kwargs):
#         app_pk = self.get_queryset()[0].pk
#         kwargs = {'pk': app_pk}
#         url = reverse('detail_app', kwargs=kwargs)
#         return HttpResponseRedirect(url)

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

class AppDemographicsView(DetailView):
    model = MobileApp
    template_name = "apps/mobileapp_demographics.html"

    def get_context_data(self, **kwargs):
        context = super(AppDemographicsView, self).get_context_data(**kwargs)
        mobileapp = context['mobileapp']
        return context

class AppSettingsView(DetailView):
    model = MobileApp
    template_name = "apps/mobileapp_settings.html"

    def get_context_data(self, **kwargs):
        context = super(AppSettingsView, self).get_context_data(**kwargs)
        mobileapp = context['mobileapp']
        return context

class AppAlgorithmsView(DetailView):
    model = MobileApp
    template_name = "apps/mobileapp_algorithms.html"

    def get_context_data(self, **kwargs):
        context = super(AppAlgorithmsView, self).get_context_data(**kwargs)
        mobileapp = context['mobileapp']
        return context

class SterlingRegistrationView(RegistrationView):

    def get_success_url(self, request, user):
        return reverse("dashboard")


