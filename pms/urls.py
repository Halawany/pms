# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('templates/', views.TemplateListView.as_view(), name='template_list'),
    path('templates/create/', views.TemplateCreateView.as_view(), name='template_create'),
    path('evaluations/', views.EvaluationListView.as_view(), name='evaluation_list'),
    path('evaluations/create/', views.EvaluationCreateView.as_view(), name='evaluation_create'),
    path('evaluations/<int:evaluation_id>/employee/<str:employee_id>/', views.EmployeeEvaluationView.as_view(), name='employee_evaluation'),
    path('approval/<int:employee_evaluation_id>/', views.ApprovalView.as_view(), name='approval'),
]