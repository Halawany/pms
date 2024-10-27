from django.urls import path
from .views import (
    EmployeeCreateView, TemplateCreateView, EvaluationCreateView, CategoryCreateView,
    MetricCreateView,EvaluationView, EmployeeScoreView, EvaluationDetailView
)

urlpatterns = [
    path('add-employee', EmployeeCreateView.as_view(), name='add-employee'),
    path('add-template', TemplateCreateView.as_view(), name='add-template'),
    path('new-evaluation', EvaluationCreateView.as_view(), name='add-evaluation'),
    path('add-category', CategoryCreateView.as_view(), name='add-category'),
    path('add-metric', MetricCreateView.as_view(), name='add-metirc'),
    path('evaluate/<int:hr_code>', EvaluationView.as_view(), name='employee-evaluation'),
    path('finalscore/<int:employee_id>', EmployeeScoreView.as_view(), name='final_score'),
    path('evaluation/<int:pk>/', EvaluationDetailView.as_view(), name='evaluation_detail'),
    # path('evalaute/<int:evaluation_id>', EvaluationView.as_view(), name='employee-evaluation'),
]
