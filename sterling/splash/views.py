# Create your views here.
from validate_email import validate_email

from apps.models import MobileApp

from django.views.generic import View
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import SignUp

class SplashFormView(View):
    template_name = "splash.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email', '')
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        
        if validate_email(email):
            signup = SignUp(email=email)
            signup.save()
            return render(request, self.template_name, {"signup_success": True})
        else:
            return render(request, self.template_name, {"error": True})

    def get_queryset(self):
        try:
            return MobileApp.objects.filter(users__exact=self.request.user)
        except TypeError:
            return None


    def dispatch(self, request, *args, **kwargs):
        if self.get_queryset():
            return redirect('apps/detail/%d' % int(self.get_queryset()[0].pk) )
        #return self.as_view()
        return render(request, self.template_name)





