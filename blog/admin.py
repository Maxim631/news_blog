from django.contrib import admin
from users.models import User
from .models import News, Comments, Category

admin.site.register(News)
admin.site.register(Comments)
admin.site.register(Category)
admin.site.register(User)