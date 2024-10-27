from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, View, DetailView, ListView
from django.db.models import Sum
from .models import Employee, Template, Evaluation, Category, Metric, UserScore
from .forms import EmployeeInsertForm, TemplateInsertForm, EvaluationForm, CategoryForm, MetricForm, UserScoreForm, UserScoreFormSet

class EmployeeCreateView(CreateView):
    model = Employee
    template_name = "pms/add-employee.html"
    form_class = EmployeeInsertForm

class TemplateCreateView(CreateView):
    model = Template
    template_name = 'pms/add-template.html'
    form_class = TemplateInsertForm

class EvaluationCreateView(CreateView):
    model = Evaluation
    template_name = 'pms/evaluation.html'
    form_class = EvaluationForm

class CategoryCreateView(CreateView):
    model = Category
    template_name = 'pms/category.html'
    form_class = CategoryForm

class MetricCreateView(CreateView):
    model = Metric
    template_name = 'pms/metirc.html'
    form_class = MetricForm


class EvaluationView(CreateView):
    model = UserScore
    template_name = 'pms/user_score.html'
    form_class = UserScoreForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        
        # Fetch the employee instance using the employee_id from URL kwargs
        employee_id = self.kwargs.get('employee_id')
        employee = get_object_or_404(Employee, id=employee_id)
        
        # Assign the employee instance to the UserScore object
        self.object.employee = employee
        self.object.save()
        
        return super().form_valid(form)

class EmployeeScoreView(ListView):
    model = UserScore
    template_name = 'pms/finalscore.html'
    context_object_name = 'user_scores'

    def get_queryset(self):
        employee_id = self.kwargs.get('employee_id')
        return UserScore.objects.filter(employee_id=employee_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employee_id = self.kwargs.get('employee_id')
        
        # Calculate the total score for the employee
        total_score = UserScore.objects.filter(employee_id=employee_id).aggregate(total_score=Sum('score'))
        context['total_score'] = total_score['total_score']  # or 0 if None

        return context
    

class EvaluationDetailView(DetailView):
    model = Evaluation
    template_name = 'pms/evaluation_detail.html'
    context_object_name = 'evaluation'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        evaluation = self.object
        
        # Fetch employees and their scores for the specific evaluation
        context['employees'] = Employee.objects.all()  # or filter as needed
        context['scores'] = UserScore.objects.filter(evaluation=evaluation).select_related('employee', 'metric')
        
        return context