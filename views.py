from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProjectForm, FeedbackForm
from .models import Feedback, Project
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages  


#  Home page
def home(request):
    return render(request, 'feedback/home.html')


# Project Submission
@login_required
def submit_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.submitted_by = request.user
            project.save()
            messages.success(request, "✅ Your project has been submitted!")  # ✅ Correct

            return redirect('dashboard')
    else:
        form = ProjectForm()
    return render(request, 'submit_project.html', {'form': form})


#  Dashboard
@login_required
def dashboard(request):
    total_projects = Project.objects.count()
    total_feedback = Feedback.objects.count()
    user_projects = Project.objects.filter(submitted_by=request.user)

    return render(request, 'feedback/dashboard.html', {
        'username': request.user.username,
        'total_projects': total_projects,
        'total_feedback': total_feedback,
        'user_projects': user_projects,
    })


#  Register
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


#  Project Detail + Feedback Submission
@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    feedbacks = Feedback.objects.filter(project=project)

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.project = project
            feedback.reviewer = request.user
            feedback.save()
            return redirect('project_detail', project_id=project.id)
    else:
        form = FeedbackForm()

    return render(request, 'feedback/project_detail.html', {
        'project': project,
        'form': form,
        'feedbacks': feedbacks,
    })
@login_required
def project_list(request):
    other_projects = Project.objects.exclude(submitted_by=request.user)
    return render(request, 'feedback/project_list.html', {'projects': other_projects})

    

@login_required
def dashboard(request):
    total_projects = Project.objects.count()
    total_feedback = Feedback.objects.count()
    user_projects = Project.objects.filter(submitted_by=request.user)
    other_projects = Project.objects.exclude(submitted_by=request.user)

    return render(request, 'feedback/dashboard.html', {
        'username': request.user.username,
        'total_projects': total_projects,
        'total_feedback': total_feedback,
        'user_projects': user_projects,
        'other_projects': other_projects,
    })








