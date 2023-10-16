from django.shortcuts import render, redirect
from .models import QuestionsModel, UserAccuracyModel, UserTestDetails, QuizConfiguration
import random
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already taken")
                return redirect("register")
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email already taken")
                return redirect("register")
            user = User.objects.create_user(
                username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
            user.save()
            accuracy = UserAccuracyModel.objects.create(
                number_of_tests=0, accuracy=0, user=user)
            accuracy.save()
            return redirect('login')
        else:
            messages.info(request, "Passwords are not matching")
            return redirect("register")
    return (render(request, 'layouts/register.html'))


def auth_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # print(password_hash==User.objects.get(password=password_hash))
        user = authenticate(username=username, password=password)
        # print(user)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.info(request, "Invalid Credentials")
            return redirect("login")
    return (render(request, 'layouts/login.html'))


@login_required
def home(request):
    user = request.user
    user_accuracy = UserAccuracyModel.objects.get(user=request.user)
    user_test_history = UserTestDetails.objects.filter(
        user=user).order_by('test_number')
    return (render(request, 'layouts/dashboard.html', {'user': user, 'user_accuracy': user_accuracy, 'user_test_history': user_test_history}))

@login_required
def instructions(request):
    return (render(request, 'layouts/instructions.html'))

@login_required
def assessment(request):
    return (render(request, 'layouts/assessment.html'))

@login_required
def start_quiz(request):
    quiz_config = QuizConfiguration.objects.last()
    print(quiz_config.number_of_questions)
    request.session['quiz_config'] = {
        'number_of_questions': quiz_config.number_of_questions,
        'marks_per_question': quiz_config.marks_per_question,
        'duration_minutes': quiz_config.duration_minutes
    }
    request.session['quiz_data'] = {
        'attempted': 0,
        'correct': 0,
        'wrong': 0,
    }
    request.session['current_question'] = 1
    request.session['score'] = 0
    request.session['question_status'] = [
        'not_visited' for _ in range(quiz_config.number_of_questions)]
    return redirect('quiz_question')

@login_required
def quiz_question(request):
    # print(request.session['question_status'])
    current_question = request.session.get('current_question', 1)
    question = QuestionsModel.objects.order_by('?').first()
    if request.method == 'POST':
        pk = request.POST.get('question_id')
        question = QuestionsModel.objects.get(pk=pk)
        user_response_id = request.POST.get('response')
        correct_answer_id = question.correct_option
        if (user_response_id):
            request.session['quiz_data']['attempted'] += 1
            request.session['question_status'][current_question-1] = 'answered'
            if user_response_id == str(correct_answer_id):
                request.session['score'] = request.session['score'] + \
                    (1*(request.session.get('quiz_config')
                     ['marks_per_question']))
                request.session['quiz_data']['correct'] += 1
            else:
                request.session['quiz_data']['wrong'] += 1
        else:
            request.session['question_status'][current_question -
                                               1] = 'not_answered'

        if current_question == request.session.get('quiz_config')['number_of_questions']:
            update_quiz_data(request)
            return redirect('quiz_result')
        else:
            request.session['current_question'] = current_question + 1
            return redirect('quiz_question')

    return render(request, 'layouts/assessment.html', {'question': question, 'current_question': current_question, 'question_status': request.session.get('question_status', []), 'duration': request.session.get('quiz_config')['duration_minutes'], 'number_of_questions': request.session.get('quiz_config')['number_of_questions']})

@login_required
def quiz_result(request):
    score = request.session.get('score', 0)
    quiz_data = request.session['quiz_data']
    total_questions = request.session['current_question']
    marks_percentage = (quiz_data['correct']/total_questions)*100
    return render(request, 'layouts/result.html', {'score': score, 'attempted': quiz_data['attempted'], 'correct': quiz_data['correct'], 'wrong': quiz_data['wrong'], 'totalQuestions': total_questions, 'marks_percentage': marks_percentage, 'total_marks': total_questions*request.session.get('quiz_config')['marks_per_question']})

@login_required
def update_quiz_data(request):
    quiz_data = request.session['quiz_data']
    total_questions = request.session['current_question']
    marks_percentage = (quiz_data['correct']/total_questions)*100
    user_accuracy_details = UserAccuracyModel.objects.get(user=request.user)
    overall_accuracy = ((user_accuracy_details.accuracy*user_accuracy_details.number_of_tests) +
                        marks_percentage)/(user_accuracy_details.number_of_tests+1)
    user_accuracy_details.accuracy = overall_accuracy
    user_accuracy_details.number_of_tests += 1
    user_accuracy_details.save()

    test_details = UserTestDetails.objects.create(user=request.user, test_number=user_accuracy_details.number_of_tests, total_test_questions=total_questions, attempted_questions=quiz_data[
                                                  'attempted'], correct_answered=quiz_data['correct'], wrong_answered=quiz_data['wrong'], total_marks=total_questions, marks_secured=quiz_data['correct']*request.session.get('quiz_config')['marks_per_question'], percentage=marks_percentage)
    test_details.save()

def auth_logout(request):
    logout(request)
    return redirect('login')
