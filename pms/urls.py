from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import CustomLoginForm
from .views import (
    EmployeeCreateView, TemplateCreateView, EvaluationListVieww, CategoryCreateView,
    MetricCreateView, evo_employee, employee_list, EvaluationCreateView,
     EvaluationUpdateView, TemplateListView, hr_approval, get_employee_score, get_approval, TemplateUpdateView, CategoryListView, 
     CategoryUpdateView, MetricListView, MetricUpdateView, evaluation_results
)

urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(form_class=CustomLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('employees/add/', EmployeeCreateView.as_view(), name='add-employee'),
    path('add-template', TemplateCreateView.as_view(), name='add-template'),
    path('templates/', TemplateListView.as_view(), name='templates'),
    path('templates/edit/<int:pk>/', TemplateUpdateView.as_view(), name='edit-template'),
    path('evaluations/', EvaluationListVieww.as_view(), name='list_evaluation'),
    path('evaluations/create/', EvaluationCreateView.as_view(), name='create_evaluation'),
    path('evaluations/edit/<int:pk>/', EvaluationUpdateView.as_view(), name='edit_evaluation'),
    path('categories/add/', CategoryCreateView.as_view(), name='add-category'),
    path('categories/edit/<int:pk>/', CategoryUpdateView.as_view(), name='edit-category'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('add-metric/', MetricCreateView.as_view(), name='add-metric'),
    path('metrics/', MetricListView.as_view(), name='metrics'),
    path('metrics/edit/<int:pk>/', MetricUpdateView.as_view(), name='edit-metric'),
    # path('finalscore/<int:employee_id>', EmployeeScoreView.as_view(), name='final_score'),
    # path('evaluation/<int:pk>/', EvaluationDetailView.as_view(), name='evaluation_detail'),
    path('employees/', employee_list, name='list_employees'),
    path('evo/<int:employee_id>/', evo_employee, name='evo-copy'),
    path('hr-approval/<int:employee_id>/', hr_approval, name='hr-approval'),
    path('employee-score/<int:employee_id>/',  get_employee_score, name='get-employee-score'),
    path('employee-approval/<int:employee_id>/',  get_approval, name='get-approval'),
    path('search-employee/', evaluation_results, name='search_employee'),
]
