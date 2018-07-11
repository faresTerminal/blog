from django.shortcuts import render, Http404, get_object_or_404, redirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.template.context_processors import csrf
from django.template import loader
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from home.forms import MyRegistrationForm, createAuthor
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


from django.contrib.auth.models import User
from django.db import models
from home.models import usercomment_db
from django.db.models import Q
from home.models import publishe_db, author
from home.forms import ArticleForm, CommentForm, createForm

from home.models import comment_put
from home.models import Module, search_master2, Module_master2
from home.forms import ModuleForm
from home.models import cherche_s1
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail
from .token import activation_token
import datetime


# Create your views here.

# open home page
def index(request):
       
        return render(request, 'home/index.html')

def prvc(request):
       
        return render(request, 'home/lawer.html')

def reset_pass(request):
       
        return render(request, 'home/reste_pass.html')


# rederct to login page
def login(request):
        c = {}
        c.update(csrf (request))
        return render_to_response('home/login.html', c)

# function to see if the username and password user there is in database        
def auth_views(request):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        

        user  = auth.authenticate(username = username, password = password)

        if user is not None:
                auth.login(request, user)
                # when user have pic profile rederect loggedin page 
                user = get_object_or_404(User, id=request.user.id)
                author_profile = author.objects.filter(name=user.id)
                if author_profile:
                       authorUser = get_object_or_404(author, name=request.user.id)
                     
                       return HttpResponseRedirect('loggedin')
                # else rederect to chose pic profile
                else:
                           
                           return HttpResponseRedirect('loggedin/profile')
                
        else: 
                messages.error(request, 'اسم المستخدم أو كلمة السر غير صحيحة', extra_tags='signup')
                return HttpResponseRedirect('/')

# create redercet  function if username and password work
def loggedin(request):

        now = datetime.datetime.now().strftime('%H:%M:%S') 
        authorUser = get_object_or_404(author, name=request.user.id)


        articles = publishe_db.objects.all().order_by('-id')
        # to search in loggedin page
        search = request.GET.get('q')
        if search:
            articles = articles.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)  | 
                Q(auther__username__icontains=search) 

            )
           



        # end search 

        paginator = Paginator(articles, 30)

        page = request.GET.get('page')
        try:
            queryset = paginator.page(page)

            
        except PageNotAnInteger:
             queryset = paginator.page(1) 
        except EmptyPage:
              queryset = paginator.page(paginator.num_pages)       
        return render_to_response('home/loggedin.html', 
                {'full_name': request.user.username, 'articles': queryset, 'last_login': request.user.last_login, 
                'date_joined': request.user.date_joined, "user": authorUser, 'now': now})



def getProfile(request):
    if request.user.is_authenticated:

        user = get_object_or_404(User, id=request.user.id)
        
        author_profile = author.objects.filter(name=user.id)
       
        if author_profile:
            authorUser = get_object_or_404(author, name=request.user.id)
         
           
            post = publishe_db.objects.filter(avatar=authorUser.id)
            # you can add here a paginator with post variable 
            paginator = Paginator(post, 12)

            page = request.GET.get('page')
            try:
                queryset = paginator.page(page)

            
            except PageNotAnInteger:
                queryset = paginator.page(1) 
            except EmptyPage:
                queryset = paginator.page(paginator.num_pages)  

            # to pass form context for change password
            form = PasswordChangeForm(request.user, request.POST)
            if request.method == 'POST':
       
               if form.is_valid():
                  user = form.save(commit = True)
                  update_session_auth_hash(request, user)  # Important!
                  messages.success(request, 'Your password was successfully updated!')
            
        
               
            
            return render(request, 'home/profile.html', {"post": queryset, "user": authorUser, 'form': form})

        else:
            form = createAuthor(request.POST or None, request.FILES or None)
            if form.is_valid():
                ins = form.save(commit = False)
                ins.name = user
                ins.save()
                
                return HttpResponseRedirect('loggedin/profile')
            return render(request, 'home/avatar.html', {"form": form})

    else:
        return render_to_response('home/login.html')

   


# change password from inside
'''
def change_password(request):
    form = PasswordChangeForm(request.user, request.POST)
    if request.method == 'POST':
       
        if form.is_valid():
            user = form.save(commit = True)
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            
        
    return render(request, 'home/profile.html', {'form': form })
'''

def change_password(request):
    if request.user.is_authenticated:
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save(commit = True)
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'تم حفظ كلمة السر الجديدة')
            return redirect('loggedin/profile')
        else:
            messages.error(request, 'تأكد من كلمة السر المدخلقة ...شكرا.')
            return redirect('loggedin/profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'home/profile.html', {"form": form })  
     
         
   


# to delete user articles
def getDelete(request, pid):
    if request.user.is_authenticated:
        post= publishe_db.objects.get(id = pid)
        post.delete()
        messages.warning(request, 'تم حذف المنشور بنجاح')
        return HttpResponseRedirect('loggedin/profile')

    else:
        return render_to_response('home/login.html')

def getUpdate(request, pid):
    if request.user.is_authenticated:
        u = get_object_or_404(author, name=request.user.id)
        post = get_object_or_404(publishe_db, id=pid)
        form = createForm(request.POST or None, request.FILES or None, instance=post)
        # delete the first article
        post.delete()
        # save the update article
        if form.is_valid():

            instance = form.save(commit=False)
            instance.auther = request.user
            instance.avatar = u
            instance.save()

            messages.success(request, 'Article is updated successfully')
            return HttpResponseRedirect('loggedin/profile')
        return render(request, 'home/new.html', {"form": form})
    else:
        return render_to_response('home/login.html')







# create rederct function if username and password invalid
def invalid_login(request):
        return render_to_response('home/invalid_login.html')

def logout(request):
        auth.logout(request)
        return render_to_response('home/index.html')

# create register function
def register_user(request):
        
    form = MyRegistrationForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.is_active = False
        instance.save()
        site=get_current_site(request)
        mail_subject="Confirmation message for me"
        message=render_to_string('home/confirm_email.html',{
            "user":instance,
            'domain':site.domain,
            'uid':instance.id,
            'token':activation_token.make_token(instance)
        })
        to_email=form.cleaned_data.get('email')
        to_list=[to_email]
        from_email=settings.EMAIL_HOST_USER
        send_mail(mail_subject, message, from_email, to_list, fail_silently=False)
        return HttpResponse("<h1>Thanks for your registration. A confirmation link was sent to your email</h1>")
    return render(request, 'home/register.html', {"form": form})
# redrect from register form to avatar html file

def send_pass_link(request):
      email = request.POST.get('email', '')
      user = auth.authenticate(email = email)
      if user is not None:
         site = get_current_site(request)
         mail_subject = "Reset Password"
         message = render_to_string('home/reset_password.html', {
             
             "user":instance,
            'domain':site.domain,
            'uid':user.id,
            'token':activation_token.make_token(user)
         })
         to_email=form.cleaned_data.get('email')
         to_list=[to_email]
         from_email=settings.EMAIL_HOST_USER
         send_mail(mail_subject, message, from_email, to_list, fail_silently=True)
         return HttpResponse("<h1>Thanks we well send you link to reset your password !</h1>")
      return render(request, 'home/reste_pass.html')

       


def register_success(request):
        return render_to_response('home/index.html')

# to pass to page to create one article     
def create_article(request):
    if request.method == "POST":
        form = createForm(request.POST or None, request.FILES or None)
        if form.is_valid():
          instance = form.save(commit = False)
          instance.save()
          return redirect ('/')
    else:
      form = createForm()
      articles = publishe_db.objects.all().order_by('-id')
        
    return render(request, 'home/new.html', {"form": form, "articles": articles})

# create function to save for publishe_db model
def publier(request):
            # create instance to take avatar pic from author model
      if request.user.is_authenticated:
        user = get_object_or_404(User, id=request.user.id)
        author_profile = author.objects.filter(name=user.id)
        authorUser = get_object_or_404(author, name=request.user.id)
        form = createForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
        # pass instance author
            instance.avatar = authorUser
        # pass instance user login
            instance.auther = request.user

            instance.save()

        #pass from data base to template
            messages.success(request, 'تم النشر')
            return HttpResponseRedirect('loggedin/new/publish')
        articles = publishe_db.objects.all().order_by('-id')[:1]
        return render(request, 'home/publish.html', {'articles': articles, 
                'last_login': request.user.last_login})
      else:
          return HttpResponseRedirect('login')


        
      




    

# get email and comment from user from idex page using this function below
def comment_from_user(request):
     
          
          email = request.POST['email']
          comment = request.POST['comment']



          put = usercomment_db(email = email, comment = comment)
          put.save()
          # must be define this url in urls py file
          messages.success(request,'شكرا لقد تم ارسال تعليقك', extra_tags='comment' )
          return HttpResponseRedirect('/')

# show the true link publish(details)
def show_article(request, id):

    art = publishe_db.objects.get(pk = id)
    add = comment_put.objects.all().filter(user_put = id).order_by('id')
    context = {
         'art': art,
         'add':add,
          }
    return render(request, 'home/publish_article.html', context)

# show the true coent id


# save comment user login in database comment_put

def save_comment(request, id):

    post = publishe_db.objects.get(id = id)
    user = get_object_or_404(User, id=request.user.id)
    author_profile = author.objects.filter(name=user.id)
    authorUser = get_object_or_404(author, name=request.user.id)
   
    
    if request.method == 'POST':
        f = CommentForm(request.POST)
        if f.is_valid():
            c = f.save(commit = False)
            c.avatar_commenter = authorUser
            c.user_put = post
            c.user_comment = request.user
            c.save()

    add = comment_put.objects.all().order_by('-id')[:1]
    context = {
      'post': post,
      
      'add':add
    
    }
    messages.warning(request, 'Comment is added successfully')   
    return render(request, 'home/publish.html', context)



# save data from index page for Module

def save_Module(request):
         # model cour GRH1
         add = Module.objects.all().order_by('-id')
         # paginator for cours
         paginator = Paginator(add, 6)

         page = request.GET.get('page')
         try:
            queryset = paginator.page(page)
         except PageNotAnInteger:
             queryset = paginator.page(1) 
         except EmptyPage:
              queryset = paginator.page(paginator.num_pages)
         #model s1
         add_s1 = cherche_s1.objects.all().order_by('-id')
         paginator1 = Paginator(add_s1, 6)

         page1 = request.GET.get('page1')
         try:
            queryset1 = paginator1.page(page1)
         except PageNotAnInteger:
             queryset1 = paginator1.page(1) 
         except EmptyPage:
              queryset1 = paginator1.page(paginator.num_pages)
         return render(request, 'home/cour.html', {'add': queryset, 'add_s1': queryset1})

def add_module(request):
         title = request.POST['title']
         sub_title = request.POST['sub_title']
         file = request.POST['file']

         instance = Module(title = title, sub_title = sub_title, file = file)

         instance.save()
         
         messages.success(request, 'Article is updated successfully')
         return render(request, 'home/index.html')
        
def add_cherche_s1(request):
         title_cherche_s1 = request.POST['title_cherche_s1']
         sub_title_cherche_s1 = request.POST['sub_title_cherche_s1']
         file_s1 = request.POST['file_s1']

         instance = cherche_s1(title_cherche_s1 = title_cherche_s1, sub_title_cherche_s1 = sub_title_cherche_s1, 
                file_s1= file_s1)

         instance.save()
         
         
         return render(request, 'home/index.html')


def save_Module2(request):
         # model cour GRH1
         add = Module_master2.objects.all().order_by('-id')
         # paginator for cours
         paginator = Paginator(add, 6)

         page = request.GET.get('page')
         try:
            queryset = paginator.page(page)
         except PageNotAnInteger:
             queryset = paginator.page(1) 
         except EmptyPage:
              queryset = paginator.page(paginator.num_pages)
         #model s1
         add_s1 = search_master2.objects.all().order_by('-id')
         paginator1 = Paginator(add_s1, 6)

         page1 = request.GET.get('page1')
         try:
            queryset1 = paginator1.page(page1)
         except PageNotAnInteger:
             queryset1 = paginator1.page(1) 
         except EmptyPage:
              queryset1 = paginator1.page(paginator.num_pages)
         return render(request, 'home/cour_master2.html', {'add': queryset, 'add_s1': queryset1})

def add_module2(request):
         title = request.POST['title']
         sub_title = request.POST['sub_title']
         file1 = request.POST['file1']

         instance = Module_master2(title = title, sub_title = sub_title, file1 = file1)

         instance.save()
         
         messages.success(request, 'Article is updated successfully')
         return render(request, 'home/index.html')
        
def add_cherche_s12(request):
         title_cherche_s1 = request.POST['title_cherche_s1']
         sub_title_cherche_s1 = request.POST['sub_title_cherche_s1']
         file_s1 = request.POST['file_s1']

         instance = search_master2(title_cherche_s1 = title_cherche_s1, sub_title_cherche_s1 = sub_title_cherche_s1, 
                file_s1= file_s1)

         instance.save()
         
         
         return render(request, 'home/index.html')
        
def activate(request, uid, token):
    try:
        user = get_object_or_404(User, pk = uid)
    except:
        raise Http404('No user faound')
    if user is not None and activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('<h1> Account is activated now you can <a href ="/home/login">login</a></h1>')
    else:
        return HttpResponse('<h3> Invalid activation Link </h3>')   
