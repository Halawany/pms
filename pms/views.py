from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView, View, DetailView, ListView
from django.db.models import Sum
from .models import Employee, Template, Evaluation, Category, Metric, Level, UserScore
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


def evaluate_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    employee_level = employee.level.name
    print(employee_level)
    # Assuming 'Non-Manager' is the level you want to filter by
    non_manager_level = Level.objects.filter(name='Non-Manager').first()
    
    if not non_manager_level and employee_level != 'Non-Manager':
        return render(request, 'pms/error.html', {'message': 'Non-Manager level not found.'})

    templates = Template.objects.filter(name='Non-Manager', evaluation__level=non_manager_level).prefetch_related('category_set__metric_set')
    
    context = {
        'employee': employee,
        'templates': templates,
    }
    return render(request, 'pms/evaluate_employee.html', context)

def submit_evaluation(request, employee_id):
    if request.method == 'POST':
        employee = get_object_or_404(Employee, id=employee_id)
        
        # Assuming you want to associate scores with a specific evaluation
        # You might want to create or retrieve an Evaluation instance first
        # Here we assume you're evaluating for a specific evaluation instance
        # Adjust accordingly to your logic (e.g., year, month, etc.)
        evaluation = Evaluation.objects.filter(level__name='Non-Manager').first()
        
        if not evaluation and employee.level.name != 'Non-Manager':
            return render(request, 'pms/error.html', {'message': 'Evaluation not found.'})

        # Process the scores
        for key, value in request.POST.items():
            if key.startswith('metric_'):
                metric_id = key.split('_')[1]
                score = int(value)

                # Fetch the metric object
                metric = get_object_or_404(Metric, id=metric_id)

                # Create or update the UserScore
                user_score, created = UserScore.objects.update_or_create(
                    employee=employee,
                    metric=metric,
                    evaluation=evaluation,
                    defaults={'score': score}
                )

        # Redirect to a success page or back to the evaluation form
        return HttpResponseRedirect(reverse('success_page'))  # Adjust this to your actual success page URL

    # Handle the case where the request is not a POST (optional)
    return HttpResponseRedirect(reverse('evaluate_employee', args=[employee_id]))


def success_page(request):
    return render(request, 'pms/success.html', {'message': 'Evaluation submitted successfully!'})

def user_score_view(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    
    # Assuming you want to display scores for a specific evaluation
    evaluation = Evaluation.objects.filter(level__name='Non-Manager').first()
    
    if not evaluation:
        return render(request, 'error.html', {'message': 'No evaluation found for this employee.'})
    
    # Fetching UserScores related to the employee and the evaluation
    user_scores = UserScore.objects.filter(employee=employee, evaluation=evaluation).select_related('metric')

    context = {
        'employee': employee,
        'evaluation': evaluation,
        'user_scores': user_scores,
    }
    
    return render(request, 'pms/user_score.html', context)