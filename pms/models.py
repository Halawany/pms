from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):
    full_name = models.CharField(max_length=500)
    hr_code = models.CharField(max_length=20, primary_key=True)
    department = models.CharField(max_length=50)
    section = models.CharField(max_length=50)
    level = models.CharField(max_length=20)

    class Mets:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
    
    def __str__(self):
        return f"{self.full_name}({self.hr_code})"
class Department(models.Model):
    department_name = models.CharField(max_length=50, primary_key=True)
    department_manager = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Departmetns'

class Section(models.Model):
    section_name = models.CharField(max_length=50, primary_key=True)
    department_name = models.ForeignKey(Department, on_delete=models.CASCADE)
    section_maanger = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Section'
        verbose_name_plural = 'Sections'

class Template(models.Model):
    template_name = models.CharField(max_length=50, primary_key=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Template'
        verbose_name_plural = 'Templates'

    def __str__(self):
        return self.template_name

class MetricCategory(models.Model):
    category_name = models.CharField(max_length=50, primary_key=True)
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    category_Weight = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = 'metric_category'
        verbose_name_plural = 'metric_categories'
    
    def __str__(self):
        return self.category_name

class Metric(models.Model):
    metric_name = models.CharField(max_length=250)
    metric_category = models.ForeignKey(MetricCategory, on_delete=models.CASCADE)
    metric_weight = models.PositiveSmallIntegerField()
    template_name = models.ForeignKey(Template, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Metric'
        verbose_name_plural = 'Metrics'
    
    def __str__(self):
        return self.metric_name

class EmployeeMetricScore(models.Model):
    metric_name = models.ForeignKey(Metric, on_delete=models.CASCADE)
    employee_name = models.ForeignKey(Employee, on_delete=models.CASCADE)
    metric_score = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = 'EmployeeMericScore'
    
    def __str__(self):
        return f"{self.employee_name} with score of {self.metric_score} in metric {self.metric_name}"

class Evaluation(models.Model):
    evaluation_status = {
        'Running': 'Running',
        'Closed': 'Closed'
    }
    evaluation_year = models.PositiveSmallIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=evaluation_status)
    evaluation_template = models.ForeignKey(Template, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Evaluation'
        verbose_name_plural = 'Evaluations'
    
    def __str__(self):
        return f"From {self.start_date} To {self.end_date} Evaluation"

class EmployeeEvaluation(models.Model):
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE)
    total_score = models.PositiveSmallIntegerField()
    evaluation_grade = models.CharField(max_length=2)
    employee_code = models.ForeignKey(Employee, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'EmployeeEvaluation'

    def __str__(self):
        return f"{self.employee_code} Evaluation Score is {self.evaluation_grade}"

class Approval(models.Model):
    employee_evaluation = models.ForeignKey(EmployeeEvaluation, on_delete=models.CASCADE)
    manager_approval = models.BooleanField(default=False)
    hr_approval = models.BooleanField(default=False)
    employee_approval = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Approval'
        verbose_name_plural = 'Approvals'

    def __str__(self):
        return f"{self.employee_evaluation} Evaluation Approval"