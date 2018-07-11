from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField





class author(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(blank = True, upload_to = 'Avatar')
   
    firstname = models.CharField(max_length = 500, blank = True, null = False)
    lastname = models.CharField(max_length = 500, blank = True, null = True)
    age = models.IntegerField(blank = True, null = True)
    gender = models.CharField(max_length = 500, blank = True, null = True)
    section = models.CharField(max_length = 500, blank = True, null = True)
    level = models.CharField(max_length = 500, blank = True, null = True)

    details = models.TextField()

    def __str__(self):
        return self.name.username

        
	
# this model to take comment from user in home page and save it in database we have email and comment
class usercomment_db(models.Model):
    
    email = models.EmailField(max_length = 500, blank = True, null = False)
    comment = models.TextField(max_length = 5500, null = True)

    def __str__(self):
        return self.email
#create class to add publication from the User
class publishe_db(models.Model):
   
    auther = models.ForeignKey(User, default = None, on_delete = models.CASCADE)
    avatar = models.ForeignKey(author, on_delete = models.CASCADE)
    title = models.CharField(max_length = 500)
    body = RichTextUploadingField( blank = True, null = False, config_name = 'special',
                                                                extra_plugins=['youtube'],
                                                                external_plugin_resources = [(
                                                                'youtube',
                                                                '/media/youtube/youtube/',
                                                                'plugin.js',

                                                                             )],
                                                                        )
    file = models.FileField(null = True, blank = True, upload_to = 'Attachment')
    date = models.DateTimeField(auto_now_add = True)
    


    def __str__(self):
        return self.title

    def snippet(self):
    	return self.title[:110]  
# create model to add comment in publish page
class comment_put(models.Model):

    user_comment = models.ForeignKey(User, default = None, on_delete = models.CASCADE)
    user_put = models.ForeignKey(publishe_db, on_delete = models.CASCADE)
    avatar_commenter = models.ForeignKey(author, on_delete = models.CASCADE)
    comment = models.TextField(max_length = 5600)
    date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.comment


# add models for  cours and search to master 1

# Cours
class Module(models.Model):
    title = models.CharField(max_length = 200)
    sub_title = models.CharField(max_length = 400)
    file = models.FileField(null = True, blank = True, upload_to = 'Cours_Master1')

    def __str__(self):
        return self.title
#Search
class cherche_s1(models.Model):
    title_cherche_s1 = models.CharField(max_length = 200)
    sub_title_cherche_s1 = models.CharField(max_length = 400)
    file_s1 = models.FileField(null = True, blank = True, upload_to = 'Search_Master1')

    def __str__(self):
        return self.sub_title_cherche_s1
# end master 1


# add models for  cours and search to master 2

# Cours
class Module_master2(models.Model):
    title = models.CharField(max_length = 200)
    sub_title = models.CharField(max_length = 400)
    file1 = models.FileField(null = True, blank = True, upload_to = 'Cours_Master2')

    def __str__(self):
        return self.title
#Search
class search_master2(models.Model):
    title_cherche_s1 = models.CharField(max_length = 200)
    sub_title_cherche_s1 = models.CharField(max_length = 400)
    file_s1 = models.FileField(null = True, blank = True, upload_to = 'Search_Master2')

    def __str__(self):
        return self.sub_title_cherche_s1
# end master 2

