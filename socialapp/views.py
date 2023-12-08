from django.shortcuts import render,redirect
from django.urls import reverse
from django.views.generic import FormView,TemplateView,CreateView,UpdateView,DetailView,ListView
from socialapp.forms import RegistrationForm,LoginForm,UserProfileForm
from django.contrib.auth import authenticate,login,logout
from django.views import View
from socialapp.models import UserProfile

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
    
class ProfileUpdateView(UpdateView):
    template_name="profile_edit.html"
    form_class=UserProfileForm
    model=UserProfile
    def get_success_url(self):
        return reverse("index")
    

class ProfileDetailView(DetailView):
    template_name="profile_detail.html"
    model=UserProfile
    context_object_name="data"

class ProfileListView(View):
    def get(self,request,*args,**kwargs):
        qs=UserProfile.objects.all().exclude(user=request.user)
        return render (request,"profile_list.html",{"data":qs})
    