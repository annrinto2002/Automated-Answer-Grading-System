from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Teacher(models.Model):
    name = models.CharField(max_length=30)
    contact = models.BigIntegerField()
    email = models.EmailField()
    User = models.ForeignKey(User, on_delete=models.CASCADE)

class Programs(models.Model):
    programs = models.CharField(max_length=300)
    status = models.CharField(max_length=30, default='Active')

class Course(models.Model):
    course = models.CharField(max_length=30)
    semesters = models.IntegerField()
    Programs = models.ForeignKey(Programs, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=30, default='Active')

class Subjects(models.Model):
    subject = models.CharField(max_length=30)
    semesters = models.IntegerField()
    Course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=30, default='Active')


class Questions(models.Model):
    Subjects = models.ForeignKey(Subjects, on_delete=models.CASCADE, null=True)
    module = models.CharField(max_length=300)
    unit = models.CharField(max_length=300)
    question = models.CharField(max_length=300)
    answer = models.CharField(max_length=300,null=True)
    difficulty = models.CharField(max_length=300)
    importance = models.CharField(max_length=300)
    mark = models.CharField(max_length=300)
    status = models.CharField(max_length=30, default='Active')
    Teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)

class Exam(models.Model):
    date = models.DateField(auto_now_add=True)
    exam = models.CharField(max_length=200)
    examDate = models.DateField()
    status = models.CharField(max_length=30, default='Active')
    Teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    Subjects = models.ForeignKey(Subjects, on_delete=models.CASCADE, null=True)


class QuestionsPaper(models.Model):
    Exam = models.ForeignKey(Exam, on_delete=models.CASCADE, null=True)
    Questions = models.ForeignKey(Questions, on_delete=models.CASCADE, null=True)
    QuestionNo = models.IntegerField()


class Student(models.Model):
    regno = models.CharField(max_length=20, null=True)
    name = models.CharField(max_length=30)
    semester = models.CharField(max_length=50, null=True)
    year = models.CharField(max_length=25, null=True)
    email = models.EmailField(max_length=50)
    contact = models.BigIntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

class StudentMark(models.Model):
    Student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    QuestionsPaper = models.ForeignKey(QuestionsPaper, on_delete=models.CASCADE, null=True)
    marks = models.CharField(max_length=30, null=True)
    status = models.CharField(max_length=30, default='Pending')
    
class UploadAnswerSheet(models.Model):
    Student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, null=True)
    answerSheet = models.FileField(upload_to='answerSheet/')
    status = models.CharField(max_length=30, default='Pending')
    mark = models.IntegerField(null=True)
    comment = models.CharField(max_length=300, null=True)
    extractedFrom = models.CharField(max_length=30, null=True)
    Teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    date = models.DateField(auto_now_add=True)
