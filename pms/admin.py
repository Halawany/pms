from django.contrib import admin

# Register your models here.
from .models import Level, Employee, Evaluation, Category, Metric, Template, Approval, FinalScore

admin.site.register(Level)
# admin.site.register(Employee)
admin.site.register(Evaluation)
admin.site.register(Category)
admin.site.register(Metric)
admin.site.register(Template)
admin.site.register(Approval)
admin.site.register(FinalScore)

class EmployeeAdminSite(admin.ModelAdmin):
    list_display = ['full_name', 'hr_code', 'level']

admin.site.register(Employee, EmployeeAdminSite)