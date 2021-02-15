from django.contrib import admin
from .models import Item, User

admin.site.register([Item, User])
