from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from .models import Category, Question
from .forms import LoginForm, RegisterForm, addQuestionform
from django.contrib import messages


def index(request):
    return render(request, 'base.html')


@login_required()
def category_page(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'category.html', context)



correct_user_answers = []

@login_required()
def play(request, pk):
    questions = Question.objects.filter(category=pk).order_by('-id')
    paginator = Paginator(questions,1)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    context = {
        'questions': questions, 
        'page_obj': page_obj,
        }

    if request.method == 'GET':

        request.session['current_page'] = request.path_info + "?page=" + request.GET.get("page", '1')
        request.session['next_page'] = request.path_info + "?page=" + str(int(request.GET.get("page", '1')) + 1)
        return render(request, 'game.html', context)
    
    if request.method == 'POST':

        if page_obj.has_next():
            user_answer = request.POST['option']
            correct_answer = request.POST.get('answerLabel')
            print('correct answer ', correct_answer)
            print('user answer: ', user_answer)
            if user_answer == correct_answer:
                correct_user_answers.append(1)
                return HttpResponseRedirect(request.session['next_page'])
            else:
                correct_user_answers.append(0)
                return HttpResponseRedirect(request.session['next_page'])
        else:
            user_answer = request.POST['option']
            correct_answer = request.POST.get('answerLabel')
            if user_answer == correct_answer:
                correct_user_answers.append(1)
            else:
                correct_user_answers.append(0)
            correct = len(correct_user_answers)
            total = len(correct_user_answers)
            correct = correct_user_answers.count(1)
            wrong = correct_user_answers.count(0)
            context = {
                'total': total,
                'correct':correct,
                'wrong': wrong,
            }
            correct_user_answers.clear()
            return render(request,'result.html',context)


def addQuestion(request):    
    if request.user.is_staff:
        form=addQuestionform()
        if(request.method=='POST'):
            form=addQuestionform(request.POST)
            if(form.is_valid()):
                form.save()
                return redirect('/')
        context={'form':form}
        return render(request,'addQuestion.html',context)
    else: 
        return redirect('index') 


def user_registration(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})
    
    if request.method == 'POST':
        form = RegisterForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have singed up successfully.')
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'register.html', {'form': form})


def login_page(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user:
                login(request, user)
                messages.success(request,f'Hi {username.title()}, welcome back!')
                return redirect('index')
        
        messages.error(request,f'Invalid username or password')
        return render(request,'login.html',{'form': form})


def logout_page(request):
    logout(request)
    messages.success(request,f'You have been logged out.')
    return redirect('index')
