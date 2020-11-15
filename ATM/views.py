from django.shortcuts import render, redirect
#from django.http import HttpResponse
#from django.http import HttpResponseRedirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import*
from .models import*

# Create your views here.
def index(request):
    form = CreateAccountForm()
    text = ""
    if request.method == 'POST':
        form = CreateAccountForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('/login')
        else:
            messages.error(request, 'Passwords must contain at least 8 characters and must match')
    context = {'form':form, 'text':text}
    return render(request, 'index.html', context)
    

def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        account = authenticate(request, username = username, password = password)
        # if account is valid, logs it in
        if account is not None:
            login(request, account)
            messages.success(request, 'Login Success!')
            return redirect('/account-panel')
        else:
            messages.error(request, 'Username OR Password is incorrect')

    return render(request, 'login.html')

def log_out(request):
	logout(request)
	return redirect('/login')

@login_required(login_url='/login')
def account_panel(request):
    card = Card.objects.all()
    context = {'card': card}
    return render(request, 'account-panel.html', context)

@login_required(login_url='login')
def card_details(request):
    name = request.GET.get('name')
    card = Card.objects.filter(card_name=name)
    context = {'card': card}
    return render(request, 'card-details.html', context)

@login_required(login_url='login')
def add_card(request):
    messageError = ""
    form = CardSignupForm()
    if request.method == 'POST':
        form = CardSignupForm(request.POST)
        if form.is_valid():
            card = form.cleaned_data.get('card_name')
            messages.success(request, 'New card ' + card + ' has been added to your account') 
            form.save()
        else:
            messages.error(request, 'Card already exists')
    context = {'form':form}
    return render(request, 'add-card.html', context)

@login_required(login_url='login')
def atm_status(request):
    context = {}
    return render(request, 'atm-status.html', context)





