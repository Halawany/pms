from django.forms import ModelForm, modelformset_factory, BaseFormSet

from .models import Employee, Template, Evaluation, Category, Metric, UserScore


class EmployeeInsertForm(ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'

class TemplateInsertForm(ModelForm):
    class Meta:
        model = Template
        fields = '__all__'

class EvaluationForm(ModelForm):
    class Meta:
        model = Evaluation
        fields = '__all__'

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class MetricForm(ModelForm):
    class Meta:
        model = Metric
        fields = '__all__'

class UserScoreForm(ModelForm):
    class Meta:
        model = UserScore
        fields = ['evaluation', 'metric', 'score']
    def __init__(self, *args, **kwargs):
        # Extract the employee_id from kwargs, assuming it's passed in
        employee_id = kwargs.pop('employee_id', None)
        super().__init__(*args, **kwargs)

        if employee_id:
            # Filter evaluations based on the employee's level
            try:
                employee = Employee.objects.get(id=employee_id)
                level = employee.level.first()  # Assuming the employee has a level
                self.fields['evaluation'].queryset = Evaluation.objects.filter(level=level)
            except Employee.DoesNotExist:
                self.fields['evaluation'].queryset = Evaluation.objects.none()

class UserScoreFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


UserScoreFormSet = modelformset_factory(UserScore, form=UserScoreForm, extra=0)  # Set extra to 0 if you're using existing UserScores


