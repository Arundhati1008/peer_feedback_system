from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from feedback.views import project_list
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('submit/', views.submit_project, name='submit_project'),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('project/<int:project_id>/', views.project_detail, name='project_detail'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('projects/',project_list, name='project_list'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


