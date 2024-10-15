from django import forms
from .models import (
   Employee, Department, Section, Template,
   MetricCategory, Metric, EmployeeMetricScore,
   Evaluation, EmployeeEvaluation, Approval
)

class EmployeeCreationForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'

class DepartmentCreationForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'

class SectionCreationForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = '__all__'

class TemplateCreationForm(forms.ModelForm):
    class Meta:
        model = Template
        fields = ['template_name',]

class MetricCategoryCreationForm(forms.ModelForm):
    class Meta:
        model = MetricCategory
        fields = '__all__'

class MetricCreationForm(forms.ModelForm):
    class Meta:
        model = Metric
        fields = '__all__'

class EmployeeMetricScoreCreationForm(forms.ModelForm):
    class Meta:
        model = EmployeeMetricScore
        fields = '__all__'

class EvaluationCreationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = '__all__'

class EmployeeEvaluationCreationForm(forms.ModelForm):
    class Meta:
        model = EmployeeEvaluation
        fields = '__all__'

class ApprovalCreationForm(forms.ModelForm):
    class Meta:
        model = Approval
        fields = '__all__'