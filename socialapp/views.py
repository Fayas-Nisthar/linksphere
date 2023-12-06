from django.shortcuts import render,redirect
from django.urls import reverse
from django.views.generic import FormView,TemplateView,CreateView
from socialapp.forms import RegistrationForm,LoginForm
from django.contrib.auth import authenticate,login,logout
from django.views import View

# Create your views here.


class SignUpView(CreateView):
    template_name="register.html"
    form_class=RegistrationForm
    def get_success_url(self):
        return reverse ("signin")
    
    # def post(self,request,*args,**kwargs):
    #     form=RegistrationForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect("register")
    #     else:
    #         return render(request,"register.html",{"form":form})

# class LoginView(TemplateView):
#     template_name="login.html"

class SigninView(FormView):
    template_name="signin.html"
    form_class=LoginForm

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user_obj=authenticate(request,username=uname,password=pwd)
            if user_obj:
                login(request,user_obj)
                print("success")
                return redirect("index") 
        print("failed")
        return render (request,"signin.html",{"form":form})
    
class IndexView(TemplateView):
    template_name="index.html"

class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")


    