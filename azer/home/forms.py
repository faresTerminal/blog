from django import forms
from django.db import models
from home.models import publishe_db, comment_put
from home.models import Module
from .models import author
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm


# add multy fields to register page
class MyRegistrationForm(UserCreationForm):
   
   email = forms.EmailField(required = True)
  
  


   class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

   def save(self, commit = True):
        user = super(MyRegistrationForm, self).save(commit = False)
       
        user.email = self.cleaned_data['email']
       

        if commit:
                user.save()
        return user 
    
    
    

# create form to pass data to publish.html
class ArticleForm(forms.Form):

        class Meta:
                model = publishe_db

class ModuleForm(forms.Form):

        class Meta:
                model = Module

class CommentForm(forms.ModelForm):

        class Meta:
                model = comment_put
                fields =['comment']

class createAuthor(forms.ModelForm):
    class Meta:
        model = author
        fields = [
            'profile_picture',
            'details',
            'firstname',
            'lastname',
            'age',
            'gender',
            'section',
            'level',
        ]
class createForm(forms.ModelForm):
    class Meta:
        model = publishe_db
        fields = [
            'title',
            'body',
            'file',
            
        ]



