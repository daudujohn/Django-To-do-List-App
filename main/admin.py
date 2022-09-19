from django.contrib import admin
from .models import Todolist, Item
# Register your models here.S
admin.site.register(Todolist)
admin.site.register(Item)