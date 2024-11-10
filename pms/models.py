from django.db import models
from django.contrib.auth.models import User

# Validations
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def score_validator(value):
    # This validator is currently not correctly accessing the instance
    # We'll need to modify it to work with the model's clean method instead
    if value < 0:
        raise ValidationError(
            _("Score cannot be negative"),
            params={"value": value},
        )

class Level(models.Model):
    name  = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Employee(models.Model):
    full_name = models.CharField(max_length=500)
    hr_code = models.CharField(max_length=50)
    joining_date = models.DateField()
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.full_name

class Template(models.Model):
    name = models.CharField(max_length=100)
    weight = models.PositiveSmallIntegerField()
    level = models.ForeignKey(Level, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Evaluation(models.Model):
    status_choices = [
        ('running', 'Running'),
        ('Completed', 'Completed'),
        ('closed', 'Closed')
    ]
    name = models.CharField(max_length=100)
    year = models.PositiveSmallIntegerField()
    month = models.PositiveIntegerField()
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=status_choices, default='running')
    evaluator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} In duration of {self.year}-{self.month}"

class Category(models.Model):
    name = models.CharField(max_length=100)
    weight = models.PositiveSmallIntegerField()
    template = models.ManyToManyField(Template)

    def __str__(self):
        return self.name

class Metric(models.Model):
    name = models.CharField(max_length=100)
    metric_weight = models.PositiveSmallIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
class UserScore(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    metric = models.ForeignKey(Metric, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField(validators=[score_validator])
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE)

    def clean(self):
    # Move the metric weight validation to the clean method
        if self.score > self.metric.metric_weight:
            raise ValidationError({
                'score': _("Score (%(value)s) cannot be greater than the metric weight (%(weight)s)") % {
                    'value': self.score,
                    'weight': self.metric.metric_weight
                }
            })

    def save(self, *args, **kwargs):
        self.full_clean()  # This will run the validators
        super().save(*args, **kwargs)