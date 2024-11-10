from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, View, DetailView, ListView, UpdateView
from django.db.models import Sum
from django.contrib import messages
from .models import Employee, Template, Evaluation, Category, Metric, Level, UserScore
from .forms import EmployeeInsertForm, TemplateInsertForm, EvaluationForm, CategoryForm, MetricForm, UserScoreForm, UserScoreFormSet, EvaluationInsertForm

class EmployeeCreateView(UserPassesTestMixin, CreateView):
    model = Employee
    template_name = "pms/add-employee.html"
    form_class = EmployeeInsertForm
    success_url = reverse_lazy('employee-list')  # Redirect after successful form submission

    # Add levels to context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['levels'] = Level.objects.all()  # Get all levels to pass to the template
        return context

    def test_func(self):
        return self.request.user.is_staff

class TemplateCreateView(CreateView):
    model = Template
    template_name = 'pms/add-template.html'
    form_class = TemplateInsertForm

class TemplateListView(ListView):
    model = Template
    template_name = 'pms/templates.html'
    context_object_name = 'templates'

class EvaluationListVieww(ListView):
    model = Evaluation
    template_name = 'pms/list_evalautions.html'
    context_object_name = 'evaluations'

class EvaluationCreateView(CreateView):
    model = Evaluation
    template_name = 'pms/create_evaluation.html'
    form_class = EvaluationInsertForm

class EvaluationUpdateView(UpdateView):
    model = Evaluation
    form_class = EvaluationInsertForm
    template_name = 'pms/edit_evaluation.html'  # Template to render the form
    context_object_name = 'evaluation'
    
    def get_success_url(self):
        # Redirect to the evaluations list after successful update
        return reverse_lazy('list_evaluation')  # You can change this URL name if necessary

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

def evo_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    employee_level = employee.level
    evaluation = get_object_or_404(Evaluation, level=employee_level)
    
    if evaluation.evaluator == request.user and evaluation.status == 'running':
        # Fetch metrics and existing scores
        metrics = Metric.objects.filter(category__template=evaluation.template.id)
        
        # Convert metric IDs to strings in the dictionary
        existing_scores = {
            str(us.metric.id): us.score 
            for us in UserScore.objects.filter(
                employee=employee, 
                evaluation=evaluation
            )
        }
        
        if request.method == 'POST':
            form = EvaluationForm(request.POST, metrics=metrics, existing_scores=existing_scores)
            if form.is_valid():
                for metric in metrics:
                    score = form.cleaned_data[f'score_{metric.id}']
                    if score > metric.metric_weight:
                        messages.error(request, 'Metric score must be less than or equal to the weight of metric.')
                        return redirect('evo-copy', employee_id=employee_id)
                    UserScore.objects.update_or_create(
                        employee=employee,
                        metric=metric,
                        evaluation=evaluation,
                        defaults={'score': score}
                    )
                messages.success(request, 'Successful evaluation.')
                return redirect('list_employees')
        else:
            form = EvaluationForm(metrics=metrics, existing_scores=existing_scores)
    else:
        return redirect('list_employees')
    
    return render(request, 'pms/copy.html', {
        'form': form,
        'employee': employee,
        'evaluation': evaluation,
        'metrics': metrics,
        'existing_scores': existing_scores,
    })

def employee_list(request):
    evaluation = Evaluation.objects.filter(evaluator=request.user.id, status='running').first()
    if evaluation:
        employee = Employee.objects.filter(level=evaluation.level.id)
        return render(request, 'pms/list_employees.html', {'employees': employee})
    else:
        messages.error(request, 'No available evaluation.')
        return redirect('list_evaluation')