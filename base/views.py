from django.shortcuts import redirect, render
from . import forms, models
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout

def index(request):
    users = models.User.objects.filter(event_participant=True)
    events = models.Event.objects.all()
    context = {'users': users,'events':events}
    return render(request,'home.html',context)

def user(request,pk):
    user=models.User.objects.get(id=pk)
    context = {'user': user}
    return render(request,'profile.html',context)

@login_required(login_url='/login')
def account(request):
    user= request.user
    context={'user': user}
    return render(request,'account.html',context)

def event(request,pk):
    event= models.Event.objects.get(id=pk)

    registered = False
    submitted = False
    
    if request.user.is_authenticated:

        registered = request.user.events.filter(id=event.id).exists()
        submitted = forms.Submission.objects.filter(participant=request.user, event=event).exists()
    context = {'event':event, 'registered':registered, 'submitted':submitted}
    return render(request, 'event.html',context)

@login_required(login_url='/login')
def event_confirmation(request,pk):
    event = models.Event.objects.get(id=pk)

    if request.method == 'POST':
        event.participants.add(request.user)
        return redirect('event', pk=event.id)

    return render(request,'event_confirmation.html', {'event':event})

@login_required(login_url='/login')
def submission(request,pk):
    event = models.Event.objects.get(id=pk)
    
    form=forms.SubmissionForm()
    
    if request.method == 'POST':
        form = forms.SubmissionForm(request.POST)

        if form.is_valid():
            submission = form.save(commit=False)
            submission.participant = request.user
            submission.event = event
            submission.save()
            
            return redirect('account')
    
    context = {'event': event,'form':form}
    return render(request,'submit_form.html',context)

@login_required(login_url='/login')
def update_submission(request, pk):
    submission = models.Submission.objects.get(id=pk)

    if request.user != submission.participant:
        return HttpResponse('You cant be here!!!!')

    event = submission.event
    form = forms.SubmissionForm(instance=submission)

    if request.method == 'POST':
        form = forms.SubmissionForm(request.POST, instance=submission)
        if form.is_valid():
            form.save()
            return redirect('account')


    context = {'form':form, 'event':event}

    return render(request, 'submit_form.html', context)

def login(request):
    page = 'login'

    if request.method == "POST":
        user = authenticate(
            email=request.POST['email'],
            password=request.POST['password']
            )

        if user is not None:
            dj_login(request, user)
            messages.info(request, 'You have succesfully logged in.')
            return redirect('home')
        else:
            messages.error(request, 'Email OR Password is incorrect')
            return redirect('login')
    
    context = {'page':page}

    return render(request, 'login_register.html', context)

def logout(request):
    dj_logout(request)
    messages.info(request, 'User was logged out!')
    return redirect('login')

def register(request):
    form = forms.CustomUserCreateForm()

    if request.method == 'POST':
        form = forms.CustomUserCreateForm(request.POST, request.FILES,)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            dj_login(request, user)
            messages.success(request, 'User account was created!')
            return redirect('home')
        else:
            messages.error(request, 'An error has occurred during registration')


    page = 'register'
    context = {'page':page, 'form':form}
    return render(request, 'login_register.html', context)
