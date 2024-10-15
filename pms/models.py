from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Employee(models.Model):
    full_name = models.CharField(max_length=500)
    hr_code = models.CharField(max_length=20, primary_key=True)
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    section = models.ForeignKey('Section', on_delete=models.CASCADE)
    level = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
    
    def __str__(self):
        return f"{self.full_name} ({self.hr_code})"

class Department(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    manager = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

    def __str__(self):
        return self.name

class Section(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    manager = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Section'
        verbose_name_plural = 'Sections'

    def __str__(self):
        return self.name

class Template(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    employee_level = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Template'
        verbose_name_plural = 'Templates'

    def __str__(self):
        return f"{self.name} (Level: {self.employee_level})"

class MetricCategory(models.Model):
    CATEGORY_TYPES = [
        ('KPI', 'Key Performance Indicator'),
        ('COMP', 'Competency'),
    ]
    name = models.CharField(max_length=50, primary_key=True)
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    weight = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    category_type = models.CharField(max_length=4, choices=CATEGORY_TYPES)

    class Meta:
        verbose_name = 'Metric Category'
        verbose_name_plural = 'Metric Categories'
    
    def __str__(self):
        return f"{self.name} ({self.get_category_type_display()})"

class Metric(models.Model):
    name = models.CharField(max_length=250)
    category = models.ForeignKey(MetricCategory, on_delete=models.CASCADE)
    weight = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    template = models.ForeignKey(Template, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Metric'
        verbose_name_plural = 'Metrics'
    
    def __str__(self):
        return f"{self.name} ({self.category.name})"

class Evaluation(models.Model):
    EVALUATION_STATUS = [
        ('Running', 'Running'),
        ('Closed', 'Closed')
    ]
    year = models.PositiveSmallIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=EVALUATION_STATUS)
    template = models.ForeignKey(Template, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Evaluation'
        verbose_name_plural = 'Evaluations'
    
    def __str__(self):
        return f"{self.year} Evaluation ({self.start_date} to {self.end_date})"

class EmployeeEvaluation(models.Model):
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    total_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    grade = models.CharField(max_length=2, null=True, blank=True)

    class Meta:
        verbose_name = 'Employee Evaluation'
        verbose_name_plural = 'Employee Evaluations'

    def __str__(self):
        return f"{self.employee} - {self.evaluation.year} Evaluation"

    def calculate_total_score(self):
        metric_scores = self.employeemetricscore_set.all()
        total_score = sum(score.weighted_score for score in metric_scores)
        self.total_score = round(total_score, 2)
        self.save()

    def calculate_grade(self):
        if self.total_score is None:
            return None
        if self.total_score >= 90:
            return 'A'
        elif self.total_score >= 80:
            return 'B'
        elif self.total_score >= 70:
            return 'C'
        elif self.total_score >= 60:
            return 'D'
        else:
            return 'F'

class EmployeeMetricScore(models.Model):
    employee_evaluation = models.ForeignKey(EmployeeEvaluation, on_delete=models.CASCADE)
    metric = models.ForeignKey(Metric, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])

    class Meta:
        verbose_name = 'Employee Metric Score'
        verbose_name_plural = 'Employee Metric Scores'
    
    def __str__(self):
        return f"{self.employee_evaluation.employee} - {self.metric.name}: {self.score}"

    @property
    def weighted_score(self):
        return (self.score * self.metric.weight) / 100

class Approval(models.Model):
    employee_evaluation = models.OneToOneField(EmployeeEvaluation, on_delete=models.CASCADE)
    manager_approval = models.BooleanField(default=False)
    hr_approval = models.BooleanField(default=False)
    employee_approval = models.BooleanField(default=False)
    manager_comments = models.TextField(blank=True)
    hr_comments = models.TextField(blank=True)
    employee_comments = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Approval'
        verbose_name_plural = 'Approvals'

    def __str__(self):
        return f"{self.employee_evaluation} Approval Status"