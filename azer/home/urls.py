"""azer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm
from .import views

app_name="home"
urlpatterns = [
    
    url(r'^$', views.index, name='index'),
    
    url(r'^comment_user/$', views.comment_from_user, name='comment_from_user'),
    url(r'^login/$', views.login, name='login'),
    url(r'^auth/$', views.auth_views, name='auth_views'),
    url(r'loggedin/$', views.loggedin, name='loggedin'),
    url(r'create/$', views.create_article, name='create_article'),
    url(r'password_change/$', views.change_password, name='change_password'),

    # urls to change password user via Email ############################################################""
    url(r'^password_reset/$', auth_views.password_reset, {"template_name": "regi/password_reset_form.html", 
        "post_reset_redirect": "password_reset_done", "email_template_name": "regi/password_reset_email.html"}, name='password_reset'),

    url(r'^password_reset/done/$', auth_views.password_reset_done, {"template_name": "regi/password_reset_done.html"}, name='password_reset_done'),
        
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, {"template_name": "regi/password_reset_confirm.html"}, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, {"template_name": "regi/password_reset_complete.html"}, name='password_reset_complete'),
    ##############################################################################################

   


    url(r'publish/$', views.publier, name='publier'),
    #put comment to publish
    url(r'comment/$', views.save_comment, name='save_comment'),


    # master 1 
    url(r'cours/$', views.save_Module, name='save_Module'),
    url(r'cours1/$', views.add_module, name='add_module'),
    url(r'cours_s1/$', views.add_cherche_s1, name='add_cherche_s1'),

    # master 2
    url(r'cours2/$', views.save_Module2, name='save_Module2'),
     url(r'cours12/$', views.add_module2, name='add_module2'),
    url(r'cours_s12/$', views.add_cherche_s12, name='add_cherche_s12'),




    url(r'prvc/$', views.prvc, name='prvc'),
    url(r'reset_password/$', views.reset_pass, name='reset_pass'),
    url(r'^password_email/$', views.send_pass_link, name='send_pass_link'),
    

    # to go to spicial id when click a link 
    url(r'article/(?P<id>\d+)/$', views.show_article, name='show_article'),
    
    url(r'add_comment/(?P<id>\d+)/$', views.save_comment, name='save_comment'),

    url(r'^invalid/$', views.invalid_login , name='invalid_login'),
    url(r'^$', views.logout, name ='logout'),
    url(r'^register/$', views.register_user, name='register_user'),
    url(r'profile/$', views.getProfile, name="getProfile"),
    url(r'delete/(?P<pid>\d+)/$', views.getDelete, name="getDelete"),
    url(r'update/(?P<pid>\d+)/$', views.getUpdate, name="getUpdate"),
    
    
    
   
    

    url(r'^register_success/$', views.register_success, name='register_success'),
    
    #account confirmations
    path('activate/<uid>/<token>', views.activate, name="activate")
    
    
]