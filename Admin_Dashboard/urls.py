from django.views.decorators.csrf import csrf_exempt
from django.urls import path
from . import views
urlpatterns = [
    path('Dashboard', views.DashboardView, name='nDashboard'),
    path('add-employee', views.AddEmployeeView, name='nadd-employee'),
    path('add-department', views.AddDepartmentView, name='nadd-department'),
    path('delete-department', views.DeleteDepartmentView, name='ndelete-department'),
    path('validate-employee-username', csrf_exempt(views.ValidateEmployeeUsernameView), name='nvalidate-employee-username'),
    path('validate-employee-email', csrf_exempt(views.ValidateEmployeeEmailView), name='nvalidate-employee-email'),
    path('Admin-Profile', views.AdminProfileView, name='nAdminProfile' )
    
]
