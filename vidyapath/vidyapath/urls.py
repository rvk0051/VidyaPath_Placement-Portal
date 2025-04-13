"""
URL configuration for vidyapath project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
#from vidyapath_project.views import *
from . import views
from .views import notice
from .views import login, home  
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.conf.urls.static import static
from .views import placement_stats, get_chart_data, get_salary_distribution, get_top_achievers ,admin_entry,delete_student,delete_company ,get_students,students_view, get_companies, add_company, add_student




urlpatterns = [
    path('',views.home,name='home'),
#    path('admin/', admin.site.urls),
    
    path('register/', views.register, name='register'),  # URL for register.html
    path('contact/', views.contact, name='contact'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('adminlogin/', views.adminlogin, name='adminlogin'),
   
    path('admindashboard/', views.admindashboard, name='admindashboard'),
    path('notice/', views.notice, name='notice'),
    path('notice/update_notice/<int:id>/', views.update_notice, name='update_notice'),
    path('notice/update_notice/update_notice1/<int:id>/', views.update_notice1, name='update_notice1'),
    path("notice/delete1/<int:id>/", views.delete1, name="delete1"),
    path("admindashboard/delete/<int:id>/", views.delete, name="delete"),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('placement/', views.placement, name='placement'),
    path('learningdev/', views.learningdev, name='learningdev'),
    path('placementg/', views.placementg, name='placementg'),
    path('placement_stats/', views.placement_stats, name='placement_stats'),
   #
   # path('signout/', views.signout, name='signout'),
    #path("signin/", LoginView.as_view(template_name="login.html"), name="signin"),
    path("signin/", views.signin, name="signin"),
    path('get_chart_data/', get_chart_data, name='get_chart_data'),
    path('get_salary_distribution/', get_salary_distribution, name='get_salary_distribution'),
    path('get_top_achievers/', get_top_achievers, name='get_top_achievers'),
    path("signin/", LoginView.as_view(template_name="login.html"), name="signin"),
    path('signout/', views.signout, name='signout'),
    path('pdf_manager/', views.pdf_manager, name='pdf_manager'),
   # path('', views.pdf_manager, name='pdf_manager'),
    path('download/<int:pdf_id>/', views.download_pdf, name='download_pdf'),
   # path('admin/',admin.site.urls),
    #path("update_notice/<int:notice_id>/", update_notice, name="update_notice"),
        path('resume_list/', views.resume_list, name='resume_list'),
        #path('', include('vidyapath_project.urls')), #or whatever your app name is
     path('placement-stats/', placement_stats, name='placement_stats'),  # API endpoint
    path('get_chart_data/', get_chart_data, name='get_chart_data'),
    path('get_salary_distribution/', get_salary_distribution, name='get_salary_distribution'),
    path('get_top_achievers/', get_top_achievers, name='get_top_achievers'),

    path("admin_entry/", views.admin_entry, name="admin_entry"),  
    path("api/get_companies/", views.get_companies, name="get_companies"),
    path("api/add_company/", views.add_company, name="add_company"),
    path("api/add_student/", views.add_student, name="add_student"),

    
    path('students/', students_view, name='students'),
    path("get-students/", get_students, name="get_students"),
    path('delete-student/<str:student_id>/', delete_student, name="delete_student"),
    path("api/get_companies/", views.get_companies, name="get_companies"),
    path("api/add_company/", views.add_company, name="add_company"),
    path("api/add_student/", views.add_student, name="add_student"),
    path('delete-company/<int:id>/', delete_company, name='delete_company'),



    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('download/<int:resume_id>/', views.download_resume, name='download_resume'),
    path('delete/<int:resume_id>/', views.delete_resume, name='delete_resume'),



] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)