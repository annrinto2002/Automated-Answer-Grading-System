"""
URL configuration for AAGS project.

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
from django.urls import path
from aagsApp import views
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index),
    path("login/", views.login),


    path('adminHome', views.adminHome),
    path('adminTeacher', views.adminTeacher),
    path('adminDeleteTeacher', views.adminDeleteTeacher),
    path('adminUpdateTeacher', views.adminUpdateTeacher),
    path('adminProgram', views.adminProgram),
    path('adminDeleteDept', views.adminDeleteDept),
    path('adminCourse', views.adminCourse),
    path('adminDeleteCourse', views.adminDeleteCourse),
    path('adminSubjects', views.adminSubjects),
    path('getcourse', views.getcourse),
    path('adminDeleteSub', views.adminDeleteSub),
    path('adminExam', views.adminExam),
    path('getsem', views.getsem),
    path('getsub', views.getsub),
    path('adminGenerateQP', views.adminGenerateQP),
    path('adminPrintQP', views.adminPrintQP),








    path('teacherHome', views.teacherHome),
    path('teAddQus', views.teAddQus),
    path('teAddQuestions', views.teAddQuestions),
    path('teViewQus', views.teViewQus),
    path('teDeleteQus', views.teDeleteQus),
    path('teViewQusPaper', views.teViewQusPaper),
    path('teStudents', views.teStudents),
    path('teDeleteStudent', views.teDeleteStudent),
    path('teUpdateStudent', views.teUpdateStudent),
    path('teAddStudentAnswerSheetWritten', views.teAddStudentAnswerSheetWritten),
    path('teAddStudentAnswerSheetPrinted', views.teAddStudentAnswerSheetPrinted),
    path('teViewResults', views.teViewResults),





    path('studentHome', views.studentHome),
    path('studentViewResult', views.studentViewResult),






    path('generateQus', views.generateQus),




]
