from django.urls import path
from .views import (
    EmployeeCreateView, TemplateCreateView, EvaluationCreateView, CategoryCreateView,
    MetricCreateView,EvaluationView, EmployeeScoreView, EvaluationDetailView,
    evaluate_employee, success_page, user_score_view, list_employees, submit_evaluation,evo_employee,
    #submit_evaluation
)

urlpatterns = [
    path('add-employee', EmployeeCreateView.as_view(), name='add-employee'),
    path('add-template', TemplateCreateView.as_view(), name='add-template'),
    path('new-evaluation', EvaluationCreateView.as_view(), name='add-evaluation'),
    path('add-category', CategoryCreateView.as_view(), name='add-category'),
    path('add-metric', MetricCreateView.as_view(), name='add-metirc'),
    # path('evaluate/<int:hr_code>', EvaluationView.as_view(), name='employee-evaluation'),
    path('finalscore/<int:employee_id>', EmployeeScoreView.as_view(), name='final_score'),
    path('evaluation/<int:pk>/', EvaluationDetailView.as_view(), name='evaluation_detail'),
    # path('evaluate/<int:evaluation_id>/<int:employee_id>/', evaluate_employee, name='evaluate_employee'),
    # path('evaluate/submit/<int:employee_id>/', submit_evaluation, name='submit_evaluation'),
    path('success/', success_page, name='success_page'),
    path('user_score/<int:employee_id>/', user_score_view, name='user_score'),
    # path('evalaute/<int:evaluation_id>', EvaluationView.as_view(), name='employee-evaluation'),
    path('employees/', list_employees, name='list_employees'),
    path('evaluate/<int:evaluation_id>/<int:employee_id>/', evaluate_employee, name='evaluate_employee'),
    path('submit_evaluation/<int:evaluation_id>/<int:employee_id>/', submit_evaluation, name='submit_evaluation'),
    path('evo/<int:employee_id>/', evo_employee, name='evo-copy'),

]
