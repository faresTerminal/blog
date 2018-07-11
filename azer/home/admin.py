from django.contrib import admin

from django.contrib.auth.models import User
from .models import usercomment_db
from .models import publishe_db
from .models import comment_put
from .models import Module, author
from .models import cherche_s1, Module, Module_master2, search_master2






# Register your mo
admin.site.register(author)
admin.site.register(Module_master2)
admin.site.register(search_master2)

admin.site.register(usercomment_db)
admin.site.register(publishe_db)
admin.site.register(comment_put)
admin.site.register(Module)
admin.site.register(cherche_s1)




