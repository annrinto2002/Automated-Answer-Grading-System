from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(QuestionsPaper)
admin.site.register(Questions)
admin.site.register(Student)
admin.site.register(UploadAnswerSheet)
admin.site.register(StudentMark)