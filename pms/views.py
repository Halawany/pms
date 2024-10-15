# views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from .models import Template, MetricCategory, Metric, Evaluation, EmployeeEvaluation, Employee, Approval
from .forms import TemplateForm, MetricCategoryForm, MetricForm, EvaluationForm, EmployeeEvaluationForm, ApprovalForm, EmployeeMetricScoreFormSet

class TemplateListView(LoginRequiredMixin, View):
    def get(self, request):
        templates = Template.objects.all()
        return render(request, 'evaluation/template_list.html', {'templates': templates})

class TemplateCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = TemplateForm()
        return render(request, 'evaluation/template_form.html', {'form': form})

    def post(self, request):
        form = TemplateForm(request.POST)
        if form.is_valid():
            template = form.save(commit=False)
            template.created_by = request.user
            template.save()
            return redirect('template_list')
        return render(request, 'evaluation/template_form.html', {'form': form})

class MetricCategoryListView(LoginRequiredMixin, View):
    def get(self, request, template_id):
        template = get_object_or_404(Template, id=template_id)
        categories = MetricCategory.objects.filter(template=template)
        return render(request, 'evaluation/metric_category_list.html', {'template': template, 'categories': categories})

class MetricCategoryCreateView(LoginRequiredMixin, View):
    def get(self, request, template_id):
        template = get_object_or_404(Template, id=template_id)
        form = MetricCategoryForm(initial={'template': template})
        return render(request, 'evaluation/metric_category_form.html', {'form': form, 'template': template})

    def post(self, request, template_id):
        template = get_object_or_404(Template, id=template_id)
        form = MetricCategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.template = template
            category.save()
            return redirect('metric_category_list', template_id=template_id)
        return render(request, 'evaluation/metric_category_form.html', {'form': form, 'template': template})

class MetricListView(LoginRequiredMixin, View):
    def get(self, request, category_id):
        category = get_object_or_404(MetricCategory, id=category_id)
        metrics = Metric.objects.filter(category=category)
        return render(request, 'evaluation/metric_list.html', {'category': category, 'metrics': metrics})

class MetricCreateView(LoginRequiredMixin, View):
    def get(self, request, category_id):
        category = get_object_or_404(MetricCategory, id=category_id)
        form = MetricForm(initial={'category': category, 'template': category.template})
        return render(request, 'evaluation/metric_form.html', {'form': form, 'category': category})

    def post(self, request, category_id):
        category = get_object_or_404(MetricCategory, id=category_id)
        form = MetricForm(request.POST)
        if form.is_valid():
            metric = form.save(commit=False)
            metric.category = category
            metric.template = category.template
            metric.save()
            return redirect('metric_list', category_id=category_id)
        return render(request, 'evaluation/metric_form.html', {'form': form, 'category': category})

class EvaluationListView(LoginRequiredMixin, View):
    def get(self, request):
        evaluations = Evaluation.objects.all().prefetch_related(
            Prefetch('employeeevaluation_set', queryset=EmployeeEvaluation.objects.select_related('employee'))
        )
        return render(request, 'evaluation/evaluation_list.html', {'evaluations': evaluations})

class EvaluationCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = EvaluationForm()
        return render(request, 'evaluation/evaluation_form.html', {'form': form})

    def post(self, request):
        form = EvaluationForm(request.POST)
        if form.is_valid():
            evaluation = form.save()
            return redirect('evaluation_list')
        return render(request, 'evaluation/evaluation_form.html', {'form': form})

class EvaluationDetailView(LoginRequiredMixin, View):
    def get(self, request, evaluation_id):
        evaluation = get_object_or_404(Evaluation, id=evaluation_id)
        return render(request, 'evaluation/evaluation_detail.html', {'evaluation': evaluation})

class EmployeeEvaluationView(LoginRequiredMixin, View):
    def get(self, request, evaluation_id, employee_id):
        evaluation = get_object_or_404(Evaluation, id=evaluation_id)
        employee = get_object_or_404(Employee, hr_code=employee_id)
        employee_evaluation, created = EmployeeEvaluation.objects.get_or_create(
            evaluation=evaluation,
            employee=employee
        )
        
        if created:
            metrics = Metric.objects.filter(template=evaluation.template)
            for metric in metrics:
                EmployeeMetricScore.objects.create(
                    employee_evaluation=employee_evaluation,
                    metric=metric,
                    score=0  # Default score
                )

        formset = EmployeeMetricScoreFormSet(instance=employee_evaluation)
        
        return render(request, 'evaluation/employee_evaluation_form.html', {
            'employee_evaluation': employee_evaluation,
            'formset': formset,
        })

    def post(self, request, evaluation_id, employee_id):
        evaluation = get_object_or_404(Evaluation, id=evaluation_id)
        employee = get_object_or_404(Employee, hr_code=employee_id)
        employee_evaluation, created = EmployeeEvaluation.objects.get_or_create(
            evaluation=evaluation,
            employee=employee
        )
        
        formset = EmployeeMetricScoreFormSet(request.POST, instance=employee_evaluation)
        
        if formset.is_valid():
            formset.save()
            employee_evaluation.calculate_total_score()
            employee_evaluation.grade = employee_evaluation.calculate_grade()
            employee_evaluation.save()
            return redirect('evaluation_detail', evaluation_id=evaluation_id)
        
        return render(request, 'evaluation/employee_evaluation_form.html', {
            'employee_evaluation': employee_evaluation,
            'formset': formset,
        })

class ApprovalView(LoginRequiredMixin, View):
    def get(self, request, employee_evaluation_id):
        employee_evaluation = get_object_or_404(EmployeeEvaluation, id=employee_evaluation_id)
        approval, created = Approval.objects.get_or_create(employee_evaluation=employee_evaluation)
        form = ApprovalForm(instance=approval)
        return render(request, 'evaluation/approval_form.html', {'form': form, 'employee_evaluation': employee_evaluation})

    def post(self, request, employee_evaluation_id):
        employee_evaluation = get_object_or_404(EmployeeEvaluation, id=employee_evaluation_id)
        approval, created = Approval.objects.get_or_create(employee_evaluation=employee_evaluation)
        form = ApprovalForm(request.POST, instance=approval)
        if form.is_valid():
            form.save()
            return redirect('evaluation_detail', evaluation_id=employee_evaluation.evaluation.id)
        return render(request, 'evaluation/approval_form.html', {'form': form, 'employee_evaluation': employee_evaluation})