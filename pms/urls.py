from django.urls import path
from .views import (
    EmployeeCreateView, TemplateCreateView, EvaluationListVieww, CategoryCreateView,
    MetricCreateView,EvaluationView, EmployeeScoreView, EvaluationDetailView,
    evaluate_employee, success_page, user_score_view, list_employees, submit_evaluation,evo_employee, employee_list, EvaluationCreateView,
    #submit_evaluation
     EvaluationUpdateView
)

urlpatterns = [
    path('employees/add/', EmployeeCreateView.as_view(), name='add-employee'),
    path('add-template', TemplateCreateView.as_view(), name='add-template'),
    path('evaluations/', EvaluationListVieww.as_view(), name='list_evaluation'),
    path('evaluations/create/', EvaluationCreateView.as_view(), name='create_evaluation'),
    path('evaluations/edit/<int:pk>/', EvaluationUpdateView.as_view(), name='edit_evaluation'),
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
    path('employees/', employee_list, name='list_employees'),
    path('evaluate/<int:evaluation_id>/<int:employee_id>/', evaluate_employee, name='evaluate_employee'),
    path('submit_evaluation/<int:evaluation_id>/<int:employee_id>/', submit_evaluation, name='submit_evaluation'),
    path('evo/<int:employee_id>/', evo_employee, name='evo-copy'),
    # path('evo/<int:employee_id>/', evo_employee, name='evo-copy'),

]
