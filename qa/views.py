from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm, UserRegistrationForm

def home(request):
    questions = Question.objects.all().order_by('-created_at')
    return render(request, 'qa/home.html', {'questions': questions})

@never_cache
@csrf_protect
def register(request):
    next_url = request.POST.get('next') or request.GET.get('next', reverse('home'))
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created successfully for {user.username}! You can now login.')
            login_url = reverse('login')
            if next_url:
                login_url += f'?next={next_url}'
            response = redirect(login_url)
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
            return response
    else:
        form = UserRegistrationForm()
    
    response = render(request, 'registration/register.html', {
        'form': form,
        'next': next_url
    })
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate, private, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    response['X-Accel-Expires'] = '0'
    return response

@login_required
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            return redirect('question_detail', pk=question.pk)
    else:
        form = QuestionForm()
    return render(request, 'qa/question_form.html', {'form': form})

def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    answers = question.answers.all().order_by('-created_at')
    if request.method == 'POST' and request.user.is_authenticated:
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.author = request.user
            answer.save()
            return redirect('question_detail', pk=pk)
    else:
        form = AnswerForm()
    return render(request, 'qa/question_detail.html', {
        'question': question,
        'answers': answers,
        'form': form
    })

@login_required
def like_answer(request, pk):
    answer = get_object_or_404(Answer, pk=pk)
    if request.user in answer.likes.all():
        answer.likes.remove(request.user)
    else:
        answer.likes.add(request.user)
    return HttpResponseRedirect(reverse('question_detail', kwargs={'pk': answer.question.pk}))

def custom_logout(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')
