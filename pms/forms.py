from django import forms
from .models import Template, MetricCategory, Metric, Evaluation, EmployeeEvaluation, EmployeeMetricScore, Approval

class TemplateForm(forms.ModelForm):
    class Meta:
        model = Template
        fields = ['name', 'employee_level']

class MetricCategoryForm(forms.ModelForm):
    class Meta:
        model = MetricCategory
        fields = ['name', 'template', 'weight', 'category_type']

class MetricForm(forms.ModelForm):
    class Meta:
        model = Metric
        fields = ['name', 'category', 'weight', 'template']

class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['year', 'start_date', 'end_date', 'status', 'template']

class EmployeeEvaluationForm(forms.ModelForm):
    class Meta:
        model = EmployeeEvaluation
        fields = ['evaluation', 'employee']

class EmployeeMetricScoreForm(forms.ModelForm):
    class Meta:
        model = EmployeeMetricScore
        fields = ['metric', 'score']

class ApprovalForm(forms.ModelForm):
    class Meta:
        model = Approval
        fields = ['manager_approval', 'hr_approval', 'employee_approval', 'manager_comments', 'hr_comments', 'employee_comments']

class MetricFormSet(forms.BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(MetricFormSet, self).__init__(*args, **kwargs)
        self.queryset = Metric.objects.none()

MetricFormSet = forms.modelformset_factory(
    Metric, form=MetricForm, formset=MetricFormSet, extra=1, can_delete=True
)

EmployeeMetricScoreFormSet = forms.inlineformset_factory(
    EmployeeEvaluation, 
    EmployeeMetricScore, 
    form=EmployeeMetricScoreForm, 
    extra=0, 
    can_delete=False
)
