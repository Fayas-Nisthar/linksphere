from django.contrib import messages
from django.shortcuts import render,redirect
from django.urls import reverse
from django.views.generic import FormView,TemplateView,CreateView,UpdateView,DetailView,ListView
from django.contrib.auth import authenticate,login,logout
from django.utils import timezone
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from socialapp.forms import RegistrationForm,LoginForm,UserProfileForm,PostForm,CommentForm,StorieForm
from socialapp.models import UserProfile,Posts,Stories
from socialapp.decorators import login_required

# Create your views here.
decs=[login_required,never_cache]

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
        messages.error(request,"Invalid credentials")
        return render (request,"signin.html",{"form":form})
    
@method_decorator(decs,name="dispatch")
class IndexView(CreateView,ListView):
    template_name="index.html"
    model=Posts
    form_class=PostForm
    context_object_name="data"
    def form_valid(self,form):
        form.instance.user=self.request.user
        return super().form_valid(form)
    def get_success_url(self):
        return reverse("index")
    def get_queryset(self):
        blocked_profiles=self.request.user.profile.block.all()
        blocked_profile_id=[pr.user.id for pr in blocked_profiles]
        qs=Posts.objects.all().exclude(user__id__in=blocked_profile_id).order_by("-created_date")
        return qs
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        current_date=timezone.now()
        context["stories"]=Stories.objects.filter(expiry_date__gte=current_date)
        followed_profiles=self.request.user.profile.following.all()
        profile_id=[pr.user.id for pr in followed_profiles]
        context["profiles"] = UserProfile.objects.all().exclude(user=self.request.user).exclude(user__username='admin').exclude(user__id__in=profile_id)
        return context
    
@method_decorator(decs,name="dispatch")
class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")
    
@method_decorator(decs,name="dispatch")
class ProfileUpdateView(UpdateView):
    template_name="profile_edit.html"
    form_class=UserProfileForm
    model=UserProfile
    def get_success_url(self):
        return reverse("index")
    
@method_decorator(decs,name="dispatch")
class ProfileDetailView(DetailView):
    template_name="profile_details.html"
    model=UserProfile
    context_object_name="data"

@method_decorator(decs,name="dispatch")
class ProfileListView(View):
    def get(self,request,*args,**kwargs):
        qs=UserProfile.objects.all().exclude(user=request.user).exclude(user__username='admin')
        return render (request,"profile_list.html",{"data":qs})

@method_decorator(decs,name="dispatch")
class FollowsView(View):
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        profile_object=UserProfile.objects.get(id=id)
        action=request.POST.get("action")
        if action == "follow":
            request.user.profile.following.add(profile_object)
        elif action == "unfollow":
            request.user.profile.following.remove(profile_object)
        return redirect("index")
    
@method_decorator(decs,name="dispatch")
class PostUploadView(CreateView):
    template_name="post_add.html"
    form_class=PostForm
    def form_valid(self,form):
        form.instance.user=self.request.user
        return super().form_valid(form)
    def get_success_url(self):
        return reverse("index")
    
@method_decorator(decs,name="dispatch")
class PostLikeView(View):
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        post_object=Posts.objects.get(id=id)
        action=request.POST.get("action")
        if action == "like":
            post_object.liked_by.add(request.user)
        elif action == "dislike":
            post_object.liked_by.remove(request.user)
        return redirect ("index")
    
@method_decorator(decs,name="dispatch")
class CommentView(CreateView):
    template_name="index.html"
    form_class=CommentForm
    def get_success_url(self):
        return reverse("index")
    def form_valid(self,form):
        id=self.kwargs.get("pk")
        post_object=Posts.objects.get(id=id)
        form.instance.user=self.request.user
        form.instance.post=post_object
        return super().form_valid(form)
    
class PostDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Posts.objects.get(id=id).delete()
        return redirect ("index")

@method_decorator(decs,name="dispatch")
class ProfileBlockView(View):
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk") 
        profile_obj=UserProfile.objects.get(id=id)
        action=request.POST.get("action")
        if action == "block":
            request.user.profile.block.add(profile_obj)
        elif action == "unblock":
            request.user.profile.block.remove(profile_obj)
        return redirect("index")


@method_decorator(decs,name="dispatch")
class StorieCreateView(View):
    def post(self,request,*args,**kwargs):
        form=StorieForm(request.POST,files=request.FILES)
        if form.is_valid():
            form.instance.user=request.user
            form.save()
            return redirect("index")
        return redirect("index")
