from django.db import models

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

    def __str__(self):
        return self.name

class Evaluation(models.Model):
    name = models.CharField(max_length=100)
    year = models.PositiveSmallIntegerField()
    month = models.PositiveIntegerField()
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)

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
    score = models.PositiveSmallIntegerField()
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE)
