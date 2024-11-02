from django.contrib import admin

# Register your models here.
from .models import Level, Employee, Evaluation, Category, Metric, Template

admin.site.register(Level)
admin.site.register(Employee)
admin.site.register(Evaluation)
admin.site.register(Category)
admin.site.register(Metric)
admin.site.register(Template)