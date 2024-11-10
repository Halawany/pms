from django.urls import path
from .views import (
    EmployeeCreateView, TemplateCreateView, EvaluationListVieww, CategoryCreateView,
    MetricCreateView,EvaluationView, EmployeeScoreView, EvaluationDetailView,
    evo_employee, employee_list, EvaluationCreateView,
    #submit_evaluation
     EvaluationUpdateView, TemplateListView
)

urlpatterns = [
    path('employees/add/', EmployeeCreateView.as_view(), name='add-employee'),
    path('add-template', TemplateCreateView.as_view(), name='add-template'),
    path('templates/', TemplateListView.as_view(), name='templates'),
    path('evaluations/', EvaluationListVieww.as_view(), name='list_evaluation'),
    path('evaluations/create/', EvaluationCreateView.as_view(), name='create_evaluation'),
    path('evaluations/edit/<int:pk>/', EvaluationUpdateView.as_view(), name='edit_evaluation'),
    path('add-category', CategoryCreateView.as_view(), name='add-category'),
    path('add-metric', MetricCreateView.as_view(), name='add-metirc'),
    path('finalscore/<int:employee_id>', EmployeeScoreView.as_view(), name='final_score'),
    path('evaluation/<int:pk>/', EvaluationDetailView.as_view(), name='evaluation_detail'),
    path('employees/', employee_list, name='list_employees'),
    path('evo/<int:employee_id>/', evo_employee, name='evo-copy'),
]
