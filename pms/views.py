from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, View, DetailView, ListView, UpdateView
from django.db.models import Sum
from django.contrib import messages
from .models import Employee, Template, Evaluation, Category, Metric, Level, UserScore, Approval, FinalScore
from .forms import EmployeeInsertForm, TemplateInsertForm, EvaluationForm, CategoryForm, MetricForm, UserScoreForm, TemplateCreateForm, EvaluationInsertForm

class EmployeeCreateView(UserPassesTestMixin, CreateView):
    model = Employee
    template_name = "pms/add-employee.html"
    form_class = EmployeeInsertForm
    success_url = reverse_lazy('employees') 

    # Add levels to context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['levels'] = Level.objects.all()
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

class TemplateUpdateView(UpdateView):
    model = Template
    template_name = 'pms/edit_template.html'
    fields = '__all__'
    success_url = 'templates'


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
    template_name = 'pms/edit_evaluation.html'  
    context_object_name = 'evaluation'
    
    def get_success_url(self):
        return reverse_lazy('list_evaluation') 

class CategoryCreateView(CreateView):
    model = Category
    template_name = 'pms/category.html'
    form_class = CategoryForm

class CategoryListView(ListView):
    model = Category
    template_name = 'pms/list_categories.html'
    context_object_name = 'categories'

class CategoryUpdateView(UpdateView):
    model = Category
    template_name = 'pms/edit_Category.html'
    fields = '__all__'
    success_url = 'categories'

class MetricCreateView(CreateView):
    model = Metric
    template_name = 'pms/metirc.html'
    form_class = MetricForm
    success_url = 'metrics'

class MetricListView(ListView):
    model = Metric
    template_name = 'pms/list_metrics.html'
    context_object_name = 'metrics'
    paginate_by = 10
    success_url = 'metrics'

    def get_queryset(self):
        queryset = super().get_queryset()
        
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        return queryset

class MetricUpdateView(UpdateView):
    model = Metric
    template_name = 'pms/edit_metric.html'
    fields = '__all__'
    success_url = 'metrics'


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
    
@login_required
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
@login_required
def employee_list(request):
    # If the user is not a staff member (i.e., not an admin or manager)
    if not request.user.is_staff:
        # Get the current evaluation running for the user's level
        evaluation = Evaluation.objects.filter(status='running').first()
        
        # If no evaluation is running, redirect back with a message or show an empty list
        if not evaluation:
            return render(request, 'pms/list_employees.html', {
                'message': 'No active evaluation found.'
            })

        # Filter employees based on the level associated with the current evaluation
        employees = Employee.objects.filter(level=evaluation.level)
    else:
        # If the user is a staff member (admin/manager), show all employees
        employees = Employee.objects.all()
        evaluation = Evaluation.objects.filter(status='running').first()

    # Prepare the final scores dictionary if there is an active evaluation
    final_scores_dict = {}
    if evaluation:
        final_scores = FinalScore.objects.filter(evaluation=evaluation)
        # Create a dictionary of final scores with the employee's hr_code as the key
        for score in final_scores:
            final_scores_dict[score.employee] = {
                'final_score': score.final_score,
                'score': score.score
            }

    # Handle search query
    search_query = request.GET.get('search', '')
    if search_query:
        employees = employees.filter(hr_code__icontains=search_query)

    # Return the appropriate employee list and evaluation information
    return render(request, 'pms/list_employees.html', {
        'employees': employees,
        'evaluation': evaluation,
        'final_scores_dict': final_scores_dict,
        'search_query': search_query
    })

@login_required
def hr_approval(request, employee_id):
    # Check if the user is HR staff
    if not request.user.is_staff:
        return redirect('list_employees/')

    # Get the employee and the evaluation
    employee = get_object_or_404(Employee, id=employee_id)
    evaluation = get_object_or_404(Evaluation, id=request.POST.get('evaluation_id'), status='Completed')

    # Check if there's already an approval for this employee and evaluation
    existing_approval = Approval.objects.filter(employee=employee, evaluation=evaluation).first()
    
    if existing_approval:
        messages.warning(request, "HR Approval already exists for this evaluation.")
        return redirect('list_employees')  # Redirect back to employee list if already approved

    # Create a new approval record
    approval = Approval.objects.create(
        employee=employee.hr_code,
        hr_approval=True,  # Mark HR approval as True
        hr=request.user,   # HR user who clicked the button
        evaluation=evaluation
    )

    # Calculate final score for the employee
    metrics = Metric.objects.filter(category__template=evaluation.template)
    total_score = 0
    total_weight = 0

    # Add up all the scores
    for metric in metrics:
        user_score = UserScore.objects.filter(employee=employee, metric=metric, evaluation=evaluation).first()
        if user_score:
            total_score += user_score.score 

    final_score_record = FinalScore.objects.create(
        employee=employee.hr_code,
        evaluation=evaluation,
        final_score=total_score,
        score=assign_grade(total_score)
    )

    messages.success(request, f"HR Approval granted for {employee.full_name}. Final score: {final_score_record.score}.")
    return redirect('list_employees')

def assign_grade(final_score):
    """Assign a grade based on the final score."""
    if final_score >= 90:
        return 'A+'
    elif final_score >= 80:
        return 'A'
    elif final_score >= 70:
        return 'B+'
    elif final_score >= 60:
        return 'B'
    elif final_score >= 50:
        return 'C'
    else:
        return 'F'

@login_required
def get_employee_score(request, employee_id):
    """View to return just the score HTML fragment"""
    try:
        employee = Employee.objects.get(id=employee_id)
        evaluation = Evaluation.objects.filter(status='Completed', level=employee.level.id).first()
        if not evaluation:
            return HttpResponse("Employee has no active evalution")
                    
        final_score = FinalScore.objects.filter(
            employee=employee.hr_code,
            evaluation_id=evaluation.id
        ).first()
        
        return render(request, 'pms/employee_score.html', {
            'final_score': final_score
        })
            
    except Employee.DoesNotExist:
        return HttpResponse("Employee not found")
    except Exception as e:
        return HttpResponse(f"Error loading score: {str(e)}")
@login_required
def get_approval(request, employee_id):
    """View to return just the approval HTML fragment"""
    try:
        employee = Employee.objects.get(id=employee_id)
        print(f"employee_id = {employee}")
        evaluation = Evaluation.objects.filter(status='Completed', level=employee.level.id).first()
        print(f"evaluation = {evaluation}")
        if not evaluation:
            return HttpResponse("Employee has no active evalution for finalscore")
                    
        approval = Approval.objects.filter(
            employee=employee.hr_code,
            evaluation=evaluation
        ).first()
        print(approval)
        return render(request, 'pms/employee_approval.html', {
            'approval': approval,
            'employee': employee,
            'evaluation': evaluation
        })
            
    except Employee.DoesNotExist:
        return HttpResponse("Employee not found")
    except Exception as e:
        return HttpResponse(f"Error loading approval: {str(e)}")

# @login_required
def evaluation_results(request):
        hr_code = request.GET.get('hr_code')
        if not hr_code:
            return render(request, 'pms/evaluation_results.html')
        evaluation = Evaluation.objects.filter(status='running').first()
        if evaluation and evaluation.evaluator == request.user:  
            employee = Employee.objects.filter(hr_code=hr_code).first()
            if employee:
                approval = Approval.objects.filter(evaluation=evaluation.id, employee=employee.hr_code).first()
                final_score = FinalScore.objects.filter(evaluation=evaluation.id, employee=employee.hr_code).first()
                print(final_score)
                if final_score:
                    return render(request, 'pms/evaluation_results.html', {
                        'employee': employee,
                        'final_score': final_score,
                        'evaluation': evaluation,
                        'approval': approval
                    })
                else:
                    message = "No evaluation result found for this employee."
                    return render(request, 'pms/evaluation_results.html', {'message': message})
            else:
                message = "Employee not found."
                return render(request, 'pms/evaluation_results.html', {'message': message})
        else:
            # If the evaluation is not running or the user is not the evaluator
            message = "You are not authorized to view this evaluation or no active evaluation exists."
            return render(request, 'pms/evaluation_results.html', {'message': message})