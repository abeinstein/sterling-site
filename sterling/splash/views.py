# Create your views here.
from validate_email import validate_email

from django.views.generic import View
from django.shortcuts import render

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







