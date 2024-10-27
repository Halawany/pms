from django.contrib import admin

# Register your models here.
from .models import Level, Employee

admin.site.register(Level)
admin.site.register(Employee)