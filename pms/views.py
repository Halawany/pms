from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, View, DetailView, ListView, UpdateView
from django.db.models import Sum
from django.contrib import messages
from .models import Employee, Template, Evaluation, Category, Metric, Level, UserScore
from .forms import EmployeeInsertForm, TemplateInsertForm, EvaluationForm, CategoryForm, MetricForm, UserScoreForm, UserScoreFormSet, EvaluationInsertForm

class EmployeeCreateView(CreateView):
    model = Employee
    template_name = "pms/add-employee.html"
    form_class = EmployeeInsertForm
    success_url = reverse_lazy('employee-list')  # Redirect after successful form submission

    # Add levels to context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['levels'] = Level.objects.all()  # Get all levels to pass to the template
        return context

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


# def evaluate_employee(request, employee_id):
#     employee = get_object_or_404(Employee, id=employee_id)
#     employee_level = employee.level.name
#     print(employee_level)
#     # Assuming 'Non-Manager' is the level you want to filter by
#     non_manager_level = Level.objects.filter(name='Non-Manager').first()
    
#     if not non_manager_level and employee_level != 'Non-Manager':
#         return render(request, 'pms/error.html', {'message': 'Non-Manager level not found.'})

#     templates = Template.objects.filter(name='Non-Manager', evaluation__level=non_manager_level).prefetch_related('category_set__metric_set')
#     # evaluation = Evaluation.objects.filter(level=employee.level.name)
    
#     context = {
#         'employee': employee,
#         'templates': templates,
#         # 'evaluation': evaluation,
#     }
#     return render(request, 'pms/evaluate_employee.html', context)

# def submit_evaluation(request, employee_id):
#     if request.method == 'POST':
#         employee = get_object_or_404(Employee, id=employee_id)
        
#         # Assuming you want to associate scores with a specific evaluation
#         # You might want to create or retrieve an Evaluation instance first
#         # Here we assume you're evaluating for a specific evaluation instance
#         # Adjust accordingly to your logic (e.g., year, month, etc.)
#         evaluation = Evaluation.objects.filter(level__name='Non-Manager').first()
        
#         if not evaluation and employee.level.name != 'Non-Manager':
#             return render(request, 'pms/error.html', {'message': 'Evaluation not found.'})

#         # Process the scores
#         for key, value in request.POST.items():
#             if key.startswith('metric_'):
#                 metric_id = key.split('_')[1]
#                 score = int(value)

#                 # Fetch the metric object
#                 metric = get_object_or_404(Metric, id=metric_id)

#                 # Create or update the UserScore
#                 user_score, created = UserScore.objects.update_or_create(
#                     employee=employee,
#                     metric=metric,
#                     evaluation=evaluation,
#                     defaults={'score': score}
#                 )

#         # Redirect to a success page or back to the evaluation form
#         return HttpResponseRedirect(reverse('success_page'))  # Adjust this to your actual success page URL

#     # Handle the case where the request is not a POST (optional)
#     return HttpResponseRedirect(reverse('evaluate_employee', args=[employee_id]))


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



def evaluate_employee(request, evaluation_id, employee_id):
    # Fetch the employee and evaluation instances
    employee = get_object_or_404(Employee, id=employee_id)
    evaluation = get_object_or_404(Evaluation, id=evaluation_id)

    # Fetch metrics related to the evaluation's template
    metrics = Metric.objects.filter(category__template=evaluation.template)

    # Fetch existing user scores for the employee and evaluation
    user_scores = {us.metric.id: us.score for us in UserScore.objects.filter(employee=employee, evaluation=evaluation)}

    if request.method == 'POST':
        # Process the submitted scores
        for metric in metrics:
            score = request.POST.get(f'score_{metric.id}')
            if score is not None:  # Ensure score is provided
                UserScore.objects.update_or_create(
                    employee=employee,
                    metric=metric,
                    evaluation=evaluation,
                    defaults={'score': score}
                )
        return redirect('list_employees')  # Redirect to your desired page after submission

    return render(request, 'pms/evaluate_employee.html', {
        'employee': employee,
        'evaluation': evaluation,
        'metrics': metrics,
        'user_scores': user_scores,
    })


def submit_evaluation(request, evaluation_id, employee_id):
    # Fetch the employee and evaluation instances
    employee = get_object_or_404(Employee, id=employee_id)
    evaluation = get_object_or_404(Evaluation, id=evaluation_id)
    status = evaluation.status
    # Fetch metrics related to the evaluation's template
    metrics = Metric.objects.filter(category__template=evaluation.template)
    if status == 'running':
        if request.method == 'POST':
            # Process the submitted scores
            for metric in metrics:
                score = request.POST.get(f'score_{metric.id}')
                if score:
                    UserScore.objects.update_or_create(
                        employee=employee,
                        metric=metric,
                        evaluation=evaluation,
                        defaults={'score': score}
                    )
            return redirect('list_employees')  # Redirect to your desired page
    else:
        return HttpResponse("Evaluation status is closed")
    return redirect('pms/evaluate_employee', evaluation_id=evaluation.id, employee_id=employee.id)  # Redirect back to the evaluation page if not POST
def list_employees(request):
    # Get all employees from the database
    employees = Employee.objects.all()

    # Create a list to hold evaluation status for each employee
    evaluations_status = []
    
    # Assuming you have a way to get a valid evaluation
    # Here, we just grab the first evaluation or you could create one
    evaluation = Evaluation.objects.first()  # Get the first evaluation as an example

    for employee in employees:
        # Check if there are evaluations linked to the employee
        evaluations = UserScore.objects.filter(employee=employee)
        if evaluations.exists():
            # If there are evaluations, append the status as 'edit'
            evaluations_status.append((employee.id, "edit"))
        else:
            # If no evaluations exist, append the status as 'evaluate'
            evaluations_status.append((employee.id, "evaluate"))

    return render(request, 'pms/list_employees.html', {
        'employees': employees,
        'evaluations_status': evaluations_status,
        'evaluation_id': evaluation.id if evaluation else None  # Pass the evaluation ID to the template
    })


# def evo_employee(request, employee_id):
#     employee = get_object_or_404(Employee, id=employee_id)
#     emp_level = employee.level
#     print(emp_level)
#     evaluation = Evaluation.objects.get(level=emp_level)
#     print(evaluation.template.id)
#     template = get_object_or_404(Template, id=evaluation.template.id)
#     print(template.name, template.id)
#     metrics = Metric.objects.filter(category__template=evaluation.template.id)
#     print(metrics)
#     for metric in metrics:
#         print(metric.name)
#     if request.method == 'POST':
#         for metric in metrics:
#             score = request.POST.get(f'score_{metric.id}')
#             print(metric)            
#             if score is not None:  
#                 UserScore.objects.update_or_create(
#                     employee=employee,
#                     metric=metric,
#                     evaluation=evaluation,
#                     defaults={'score': score}
#                 )
#         return redirect('list_employees') 

#     return render(request, 'pms/copy.html', {
#         'employee': employee,
#         'evaluation': evaluation,
#         'metrics': metrics,
        
#     })


# def evo_employee(request, employee_id):
#     employee = get_object_or_404(Employee, id=employee_id)
#     employee_level = employee.level
    
#     try:
#         evaluation = Evaluation.objects.get(level=employee_level)
#         template = get_object_or_404(Template, id=evaluation.template.id)
#     except Evaluation.DoesNotExist:
#         return HttpResponseNotFound("Evaluation not found.")
    
#     metrics = Metric.objects.filter(category__template=evaluation.template.id)

#     if request.method == 'POST':
#         for metric in metrics:
#             score = request.POST.get(f'score_{metric.id}')
#             if score is not None:
#                 try:
#                     score_value = float(score)  # Convert score to float
#                     UserScore.objects.update_or_create(
#                         employee=employee,
#                         metric=metric,
#                         evaluation=evaluation,
#                         defaults={'score': score_value}
#                     )
#                 except ValueError:
#                     # Handle invalid score input, e.g., log or notify user
#                     print(f"Invalid score for metric {metric.id}: {score}")

#         messages.success(request, 'Scores updated successfully.')  # Feedback message
#         return redirect('list_employees') 

#     return render(request, 'pms/copy.html', {
#         'employee': employee,
#         'evaluation': evaluation,
#         'metrics': metrics,
#     })

def evo_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    employee_level = employee.level
    evaluation = get_object_or_404(Evaluation, level=employee_level)
    
    # Fetch metrics and existing scores
    metrics = Metric.objects.filter(category__template=evaluation.template.id)
    existing_scores = {us.metric.id: us.score for us in UserScore.objects.filter(employee=employee, evaluation=evaluation)}

    if request.method == 'POST':
        form = EvaluationForm(request.POST, metrics=metrics, existing_scores=existing_scores)
        if form.is_valid():
            for metric in metrics:
                score = form.cleaned_data[f'score_{metric.id}']
                UserScore.objects.update_or_create(
                    employee=employee,
                    metric=metric,
                    evaluation=evaluation,
                    defaults={'score': score}
                )
            messages.success(request, 'Scores updated successfully.')
            return redirect('list_employees')
    else:
        form = EvaluationForm(metrics=metrics, existing_scores=existing_scores)

    return render(request, 'pms/copy.html', {
        'form': form,
        'employee': employee,
        'evaluation': evaluation,
    })

def employee_list(request):
    employee = Employee.objects.all()
    return render(request, 'pms/list_employees.html', {'employees': employee})