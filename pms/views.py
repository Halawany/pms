from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView
from .forms import (
    EmployeeCreationForm, DepartmentCreationForm, SectionCreationForm, TemplateCreationForm,
    MetricCategoryCreationForm, MetricCreationForm, EmployeeMetricScoreCreationForm,
    EvaluationCreationForm, EmployeeEvaluationCreationForm, ApprovalCreationForm
)
from .models import (
    Employee, Department, Section, Template, MetricCategory, Metric,
    EmployeeMetricScore, Evaluation, EmployeeEvaluation, Approval
)

class EmployeeCreateView(CreateView):
    model = Employee
    form_class = EmployeeCreationForm
    template_name = 'pms/create_employee.html'

class DepartmentCreateView(CreateView):
    model = Department
    form_class = DepartmentCreationForm
    template_name = 'pms/create_department.html' 

class SectionCreateView(CreateView):
    model = Section
    form_class = SectionCreationForm
    template_name = 'pms/create_section.html'

class TemplateCreateView(CreateView):
    model = Template
    form_class = TemplateCreationForm
    template_name = 'pms/create_template.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class MetricCategoryCreateView(CreateView):
    model = MetricCategory
    form_class = MetricCategoryCreationForm
    template_name = 'pms/create_category.html'

class MetricCreateView(CreateView):
    model = Metric
    form_class = MetricCreationForm
    template_name = 'pms/create_metric.html'

class EmployeeMetricScoreCreateView(CreateView):
    model = EmployeeMetricScore
    form_class = EmployeeMetricScoreCreationForm
    template_name = 'pms/employeemetricscore.html'

class EvaluationCreateView(CreateView):
    model = Evaluation
    form_class = EvaluationCreationForm
    template_name = 'pms/evaluation.html'

class EmployeeEvaluationCreateView(CreateView):
    model = EmployeeEvaluation
    form_class = EmployeeEvaluationCreationForm
    template_name = 'pms/employee_evaluation.html'

class ApprovalCreateView(CreateView):
    model = Approval
    form_class = ApprovalCreationForm
    template_name = 'pms/approval.html'