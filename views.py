from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate
from django.db.models import Sum
from .models import *
import json
from django.db.models import Q
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
# Create your views here.


def index(request):
    return render(request, "index.html")


def contact(request):
    return render(request, 'contact.html')


def login(request):
    if request.POST:
        uname = request.POST["name"]
        pwd = request.POST["pass"]
        user = authenticate(username=uname, password=pwd)
        if user is None:
            messages.info(request, 'Username or password is incorrect')
        else:
            userdata = User.objects.get(username=uname)
            if userdata.is_superuser == 1:
                return redirect("/adminHome")
            elif userdata.is_staff == 1:
                request.session["email"] = uname
                r = Teacher.objects.get(email=uname)
                request.session["id"] = r.id
                request.session["name"] = r.name
                return redirect("/teacherHome")
            else:
                request.session["email"] = uname
                r = Student.objects.get(email=uname)
                request.session["id"] = r.id
                request.session["name"] = r.name
                return redirect("/studentHome")

    return render(request, "login.html")


def adminHome(request):
    return render(request, "adminHome.html")


def echome(request):
    return render(request, "echome.html")


def teacherHome(request):
    return render(request, "teacherHome.html")

######################################################################
#                           ADMIN PAGES

######################################################################


def adminTeacher(request):
    if request.POST:
        name = request.POST["name"]
        email = request.POST["email"]
        contact = request.POST["contact"]
        password = request.POST['password']

        User_exist = User.objects.filter(username=email).exists()
        if not User_exist:
            try:
                u = User.objects.create_user(
                        username=email, password=password, is_superuser=0, is_active=1, is_staff=1)
                u.save()
                r = Teacher.objects.create(
                    name=name, email=email, contact=contact,User=u)
                r.save()
            except Exception as e:
                messages.info(request, e)
            else:
                messages.info(request, 'Registration successful')
        else:
            messages.info(request, 'Email already registered')
    data = Teacher.objects.all()
    return render(request, "adminTeacher.html", {"data": data})


def adminDeleteTeacher(request):
    id = request.GET.get("id")
    User.objects.filter(id=id).delete()
    return redirect("/adminTeacher")


def adminUpdateTeacher(request):
    id = request.GET.get("id")
    data = Teacher.objects.get(id=id)
    if request.POST:
        name = request.POST["name"]
        email = request.POST["email"]
        contact = request.POST["contact"]
        try:
            Teacher.objects.filter(id=id).update(
                name=name, email=email, contact=contact)
        except Exception as e:
            messages.info(request, e)
        else:
            messages.info(request, "Updation successfull")
            return redirect("/adminTeacher")
    return render(request, "adminUpdateTeacher.html", {"data": data})

def adminProgram(request):
    if request.POST:
        department = request.POST["department"]
        if Programs.objects.filter(programs=department).exists():
            messages.info(request, 'Department already exists')
        else:
            
            dept = Programs.objects.create(programs=department)
            dept.save()
            messages.info(request, 'Department added')
    data = Programs.objects.all()
    return render(request, "adminProgram.html", {"data": data})

def adminDeleteDept(request):
    id = request.GET['id']
    data = Programs.objects.get(id=id)
    data.delete()
    return redirect("/adminProgram")

def adminCourse(request):
    if request.POST:
        course = request.POST["course"]
        sem = request.POST["sem"]
        dept = request.POST["dept"]
        de = Programs.objects.get(id=dept)
        if Course.objects.filter(course=course).exists():
            messages.info(request, 'Course already exists')
        else:
            co = Course.objects.create(course=course, semesters=sem, Programs=de)
            co.save()
            messages.info(request, 'Course added')
    data = Course.objects.all()
    depts = Programs.objects.all()
    return render(request, "adminCourse.html", {"data": data, "depts":depts})

def adminDeleteCourse(request):
    id = request.GET['id']
    data = Course.objects.get(id=id)
    data.delete()
    return redirect("/adminCourse")

def adminSubjects(request):
    if request.POST:
        course = request.POST["course"]
        sem = request.POST["sem"]
        subject = request.POST["subject"]
        co = Course.objects.get(id=course)
        if Subjects.objects.filter(semesters=sem,subject=subject,Course=co).exists():
            messages.info(request, 'Subject already exists')
        else:
            su = Subjects.objects.create(semesters=sem, Course=co,subject=subject)
            su.save()
            messages.info(request, 'Subject added')
    data = Subjects.objects.all()
    depts = Programs.objects.all()
    return render(request, "adminSubjects.html", {"data": data, "depts":depts})

def adminDeleteSub(request):
    id = request.GET['id']
    data = Subjects.objects.get(id=id)
    data.delete()
    return redirect("/adminSubjects")

def getcourse(request):
    y = request.GET.get("id")
    data = Course.objects.filter(Programs=y)
    print(data)
    datas = []
    for d in data:
        datas.append((d.id, d.course))
    jsonStr = json.dumps(datas)
    print(jsonStr)
    return HttpResponse(jsonStr)

def getsub(request):
    y = request.GET.get("id")
    course = request.GET.get("course")
    data = Subjects.objects.filter(Course=course,semesters=y)
    print(data)
    datas = []
    for d in data:
        datas.append((d.id, d.subject))
    jsonStr = json.dumps(datas)
    print(jsonStr)
    return HttpResponse(jsonStr)

def getsem(request):
    y = request.GET.get("id")
    data = Course.objects.get(id=y)
    print(data)
    datas = data.semesters
    jsonStr = json.dumps(datas)
    print(jsonStr)
    return HttpResponse(jsonStr)

def adminExam(request):
    if request.POST:
        exam = request.POST["exam"]
        course = request.POST["course"]
        examDate = request.POST["examDate"]
        teacher = request.POST["teacher"]
        sub = request.POST["sub"]
        te = Teacher.objects.get(id=teacher)
        co = Course.objects.get(id=course)
        su = Subjects.objects.get(id=sub)
        if Exam.objects.filter(exam=exam).exists():
            messages.info(request, 'Exam already exists')
        else:
            ex = Exam.objects.create(exam=exam, Subjects=su, examDate=examDate, Teacher=te)
            ex.save()
            messages.info(request, 'Exam added')
    data = Teacher.objects.filter()
    depts = Programs.objects.all()
    exams = Exam.objects.all()
    qps = []
    ques = QuestionsPaper.objects.all()
    for q in ques:
        qps.append(q.Exam.id)
    return render(request, "adminExam.html", {"data": data, "depts":depts,"exams":exams,"qps":qps})

def adminDeleteExam(request):
    id = request.GET['id']
    data = Exam.objects.get(id=id)
    data.delete()
    return redirect("/adminExam")

def adminGenerateQP(request):
    id = request.GET['id']
    exam = Exam.objects.get(id=id)
    sub = exam.Subjects
    sections = [
        {'marks': 5, 'count': 4},
        {'marks': 15, 'count': 4}
    ]
    question_no = 1
    for section in sections:
        marks = section['marks']
        count = section['count']

        # Fetch random questions based on criteria
        questions = Questions.objects.filter(
            mark=marks,
            Subjects=sub,
            difficulty__in=['Easy', 'Medium', 'Hard'],
            importance__in=['Level 1', 'Level 2', 'Level 3']
        ).order_by('?')[:count]

        print(f'Section {marks} Marks:')
        
        # Bulk create QuestionPaper entries
        question_papers = []
        for question in questions:
            question_papers.append(QuestionsPaper(Exam=exam, Questions=question, QuestionNo=question_no))
            print(f'{question_no}. {question.question} {question.mark} -- {question.difficulty} -- {question.importance} -- {question.Subjects.subject}')
            question_no += 1 
        
        QuestionsPaper.objects.bulk_create(question_papers)


        print()
    return redirect("/adminExam")

def adminPrintQP(request):
    id = request.GET['id']
    exam = Exam.objects.get(id=id)
    data = QuestionsPaper.objects.filter(Exam=exam)
    return render(request, "adminPrintQP.html", {"exam": exam, "data": data})








######################################################################
#                           Teacher PAGES

######################################################################


def teAddQus(request):
    depts = Programs.objects.all()
    return render(request, "teAddQus.html", {"depts":depts})

def teAddQuestions(request):
    sub = request.GET['sub']
    su = Subjects.objects.get(id=sub)
    tid = request.session["id"]
    if request.POST:
        module = request.POST['module']
        unit = request.POST['unit']
        question = request.POST['question']
        answer = request.POST['answer']
        difficulty = request.POST['difficulty']
        importance = request.POST['importance']
        mark = request.POST['mark']
        qu = Questions.objects.create(question=question, unit=unit, difficulty=difficulty,module=module,importance=importance,mark=mark,Subjects=su,answer=answer,Teacher=Teacher.objects.get(id=tid))
        qu.save()
    return render(request, "teAddQuestions.html", {"su":su})

def teViewQus(request):
    tid = request.session["id"]
    data = Questions.objects.filter(Teacher=tid)
    if request.POST:
        search = request.POST["search"]
        data = Questions.objects.filter(Q(Teacher=tid) & Q(Q(Subjects__subject__contains=search) | Q(question__contains=search) | Q(module=search) | Q(unit=search)))
    return render(request, "teViewQus.html", {"data":data})

def teDeleteQus(request):
    id = request.GET['id']
    data = Questions.objects.get(id=id)
    data.delete()
    return redirect("/teViewQus")

def generateQus(request):
    import random
    from faker import Faker
    fake = Faker()
    
    modules = [1,2,3,4,5]
    units = [1,2,3,4,5]
    
    difficulties = ['Easy', 'Medium', 'Hard']
    importances = ['Level 1', 'Level 2', 'Level 3']
    marks = [5, 15]
    tid = request.session["id"]
    for _ in range(1000):
        subjects = Subjects.objects.get(id=1)
        teacher = Teacher.objects.get(id=tid)
        module = random.choice(modules)
        unit = random.choice(units)
        questions = fake.word()
        answer = fake.word()
        difficulty = random.choice(difficulties)
        importance = random.choice(importances)
        mark = random.choice(marks)

        Questions.objects.create(
            Teacher=teacher,
            Subjects=subjects,
            module=module,
            unit=unit,
            question=questions,
            answer=answer,
            difficulty=difficulty,
            importance=importance,
            mark=mark
        )

    return redirect("/teAddQus")




def teViewQusPaper(request):
    uid = request.session['id']
    print(uid)
    qus = QuestionsPaper.objects.filter(Exam__Teacher=uid)
    eids = set()
    for q in qus:
        eids.add(q.Exam.id)
    data = Exam.objects.filter(Teacher=uid)
    print(data)
    return render(request, "teViewQusPaper.html", {"data":data})

def teStudents(request):
    data = ''
    if request.POST:
        regno = request.POST["regno"]
        name = request.POST["name"]
        semester = request.POST["semester"]
        year = request.POST["year"]
        email = request.POST["email"]
        contact = request.POST["contact"]
        course = request.POST["course"]
        password = request.POST["password"]
        co = Course.objects.get(id=course)
        if Student.objects.filter(regno=regno).exists():
            messages.info(request, 'Register No. already registered')
        else:
            user = User.objects.create_user(username=email, password=password, is_superuser=0, is_active=1, is_staff=0)
            user.save()
            st = Student.objects.create(regno=regno,name=name,semester=semester,year=year,email=email,contact=contact,course=co)
            st.save()
            messages.info(request, 'Student added')
    courses = Course.objects.all()
    data = Student.objects.all()
    return render(request, "teStudents.html", {"data":data, "courses":courses})
    

def teDeleteStudent(request):
    id = request.GET['id']
    data = User.objects.get(id=id)
    data.delete()
    return redirect("/teStudents")


def teUpdateStudent(request):
    id = request.GET['id']
    data = Student.objects.get(id=id)
    if request.POST:
        regno = request.POST["regno"]
        name = request.POST["name"]
        semester = request.POST["semester"]
        year = request.POST["year"]
        email = request.POST["email"]
        contact = request.POST["contact"]
        course = request.POST["course"]
        co = Course.objects.get(id=course)
        try:
            Student.objects.filter(id=id).update(regno=regno,name=name,semester=semester,year=year,email=email,contact=contact,course=co)
            User.objects.filter(id=data.user.id).update(username=email)
        except Exception as e:
            messages.info(request, e)
        else:
            messages.info(request, "Updation successfull")
            return redirect("/teStudents")
    courses = Course.objects.all()
    return render(request, "teUpdateStudent.html", {"data": data, "courses":courses})

def teAddStudentAnswerSheetWritten(request):
    id = request.GET['id']
    qp = Exam.objects.get(id=id)
    uid = request.session['id']
    tec = Teacher.objects.get(id=uid)
    if request.POST:
        student = request.POST["student"]
        st = Student.objects.get(id=student)
        answerSheet = request.FILES["answerSheet"]
        upAns = UploadAnswerSheet.objects.create(Student=st, exam=qp, answerSheet=answerSheet,Teacher=tec,extractedFrom='Written')
        upAns.save()
        from .extractAnswerWritten import extract_answers
        im_path = f"{BASE_DIR}/aagsApp/static/media/{upAns.answerSheet}"
        extracted_text = extract_answers(im_path)
        print(extracted_text)

        st = ''
        qus = QuestionsPaper.objects.filter(Exam=qp)

        for q in qus:
            from .compareAnswers import compare_answers
            answer_key = q.Questions.answer
            if q.QuestionNo in  extracted_text.keys():
                student_answer = extracted_text[q.QuestionNo]
                similarity_percentage = compare_answers(answer_key, student_answer)
                print(f"Similarity: {similarity_percentage}%")
                sm = StudentMark.objects.create(Student=upAns.Student, QuestionsPaper=q, marks=similarity_percentage)
                sm.save()
                st += f"Similarity for Q{q.QuestionNo}: {similarity_percentage}%    \n"
        upAns.status = 'Completed'
        upAns.comment = st
        upAns.save()
        return redirect("/teViewQusPaper")
    sts = UploadAnswerSheet.objects.filter(exam=qp,extractedFrom='Written')
    students = []
    for s in sts:
        students.append(s.Student.id)
    data = Student.objects.filter(course=qp.Subjects.Course).exclude(id__in=students)
    return render(request, "teAddStudentAnswerSheetWritten.html", {"data":data})

def teAddStudentAnswerSheetPrinted(request):
    id = request.GET['id']
    qp = Exam.objects.get(id=id)
    uid = request.session['id']
    tec = Teacher.objects.get(id=uid)
    if request.POST:
        student = request.POST["student"]
        st = Student.objects.get(id=student)
        answerSheet = request.FILES["answerSheet"]
        upAns = UploadAnswerSheet.objects.create(Student=st, exam=qp, answerSheet=answerSheet,Teacher=tec,extractedFrom='Printed')
        upAns.save()
        from .extractFromPdf import extract_answers
        im_path = f"{BASE_DIR}/aagsApp/static/media/{upAns.answerSheet}"
        extracted_text = extract_answers(im_path)
        print(extracted_text)
        print("=====================================")
        print("=====================================")
        st = ''
        qus = QuestionsPaper.objects.filter(Exam=qp)
        print("------------------------------------------------")
        print(qus)
        print("------------------------------------------------")
        total_mark = 0
        for q in qus:
            print("---------------------------------------------------")
            from .compareAnswers import compare_answers
            answer_key = q.Questions.answer
            max_mark = int(q.Questions.mark)
            if q.QuestionNo not in  extracted_text.keys():
                continue
            student_answer = extracted_text[q.QuestionNo]
            similarity_percentage = compare_answers(answer_key, student_answer)
            gotten_mark = (similarity_percentage/100) * max_mark
            print(f"Similarity: {similarity_percentage}%, Mark: {gotten_mark}")
            sm = StudentMark.objects.create(Student=upAns.Student, QuestionsPaper=q, marks=gotten_mark)
            sm.save()
            st += f"Q{q.QuestionNo}: {similarity_percentage}%   "
            total_mark += gotten_mark
        upAns.mark = total_mark
        upAns.status = 'Completed'
        upAns.comment = st
        upAns.save()
        return redirect("/teViewQusPaper")
    sts = UploadAnswerSheet.objects.filter(exam=qp,extractedFrom='Printed')
    students = []
    for s in sts:
        students.append(s.Student.id)
    data = Student.objects.filter(course=qp.Subjects.Course).exclude(id__in=students)
    return render(request, "teAddStudentAnswerSheetPrinted.html", {"data":data})

def teViewResults(request):
    uid = request.session['id']
    of = request.GET['for']
    data = StudentMark.objects.filter(QuestionsPaper__Exam__Teacher=uid)
    data2 = UploadAnswerSheet.objects.filter(Teacher=uid,extractedFrom=of)
    return render(request, "teViewResults.html", {"data":data2})


def studentHome(request):
    return render(request, "studentHome.html")



def studentViewResult(request):
    uid = request.session['id']
    data = UploadAnswerSheet.objects.filter(Student=uid)
    return render(request, "studentViewResult.html", {"data":data})






