from django.urls import path
from .views import (
    EmployeeCreateView, DepartmentCreateView, SectionCreateView, TemplateCreateView,
    MetricCategoryCreateView, MetricCreateView, MetricCreateView,
    EmployeeMetricScoreCreateView, EvaluationCreateView, 
    EmployeeEvaluationCreateView, ApprovalCreateView
)

urlpatterns = [
    path('newemployee/', EmployeeCreateView.as_view(), name='new-employee'),
    path('newdepartment/', DepartmentCreateView.as_view(), name='new-department'),
    path('newsection/', SectionCreateView.as_view(), name='new-section'),
    path('newtemplate/', TemplateCreateView.as_view(), name='new-template'),
    path('newcategory/', MetricCategoryCreateView.as_view(), name='new-category'),
    path('newmetric/', MetricCreateView.as_view(), name='new-metric'),
    path('employeemetricscore/', EmployeeMetricScoreCreateView.as_view(), name='new-score-record'),
    path('evaluation/', EvaluationCreateView.as_view(), name='evaluation'),
    path('employeeevaluation/', EmployeeEvaluationCreateView.as_view(), name='employee-evaluation'),
    path('approval/', ApprovalCreateView.as_view(), name='employee-approval'),
    
]

