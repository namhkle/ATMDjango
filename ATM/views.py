from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import*
from .models import*

def user_login(request):
    form = UserLogin()
    if request.method == 'POST':
        account_name = request.POST.get('Account Name')
        password = request.POST.get('Password')
        if Account.objects.filter(account_name=account_name).exists() and Account.objects.filter(password=password).exists():
            messages.success(request,'Login Success!')
            return redirect('/user-account-panel')
        else:
            messages.error(request,'Account name OR Password is incorrect!')
    context = {'form':form,}
    return render(request, 'user-login.html', context)

def user_log_out(request):
	logout(request)
	return redirect('/user-login')

@login_required(login_url='/admin-login')
def user_account_panel(request):
    card = Card.objects.all()
    account = Account.objects.all()
    
    context = {'card': card, 'account':account}
    return render(request, 'user-account-panel.html', context)


def deposit(request):
    if request.method == 'POST':
        user_pin = request.POST.get('Pin')
        user_card_number = request.POST.get('Your Card Number')      # gets user input for card number
        amount = request.POST.get('Amount')                          # gets user input for amount
    
        # Cash deposit: Validatation - checks if card number and pin exist and verify user's balance 
        if Card.objects.filter(card_number=user_card_number).exists(): 

            # gets user pin,balance, card name based on user's card number input
            user_card_name = Card.objects.get(card_number=user_card_number).card_name 
            userCardObject = Card.objects.get(card_number=user_card_number) #*important*


            # performs deposit
            userCardObject.balance += int(amount)
            userCardObject.save()#*this is how it actually saves*            


            messages.success(request, 'Deposit Success! ' + '$'+ amount + ' has been depositted from card: ' + user_card_name)   

        else:
            messages.error(request, 'Card Number or Pin is incorrect')

    return render(request, 'deposit.html')


def withdrawal(request):
    if request.method == 'POST':
        user_pin = request.POST.get('Pin')
        user_card_number = request.POST.get('Your Card Number')      # gets user input for card number
        amount = request.POST.get('Amount')                          # gets user input for amount
    
        # Cash withdrawal: Validatation - checks if card number and pin exist and verify user's balance 
        if Card.objects.filter(card_number=user_card_number).exists(): 

            # gets user pin,balance, card name based on user's card number input
            user_balance = Card.objects.get(card_number=user_card_number).balance  
            user_card_name = Card.objects.get(card_number=user_card_number).card_name 
            userCardObject = Card.objects.get(card_number=user_card_number) #*important*


            if int(amount) <= user_balance:
                # performs withdrawal
                userCardObject.balance -= int(amount)
                userCardObject.save()#*this is how it actually saves*    

                messages.success(request, 'Withdrawal Success! ' + '$'+ amount + ' has been withdrawn from card: ' + user_card_name)   
            else:
                messages.error(request, 'Insufficient Balance')
        else:
            messages.error(request, 'Card Number or Pin is incorrect')

    return render(request, 'withdrawal.html')

def transfer(request):
    if request.method == 'POST':   
        user_pin = request.POST.get('Pin')
        user_card_number = request.POST.get('Your Card Number')      # gets user input for card number
        amount = request.POST.get('Amount')                          # gets user input for amount

        # Transfer Validation - checks if user's and receiver's card number exist and verify user pin & balance 
        if Card.objects.filter(card_number=user_card_number).exists():

            # gets user balance based on user's card number input
            user_balance = Card.objects.get(card_number=user_card_number).balance
            # gets user card name based on user's card number input
            user_card_name = Card.objects.get(card_number=user_card_number).card_name 
            # get receiver's account based on user input
            receiver_card_number = request.POST.get('Receiver Card number') 
            # get user pin based on user's card number input
            pin_number = Card.objects.get(card_number=user_card_number).pin

            if user_pin != pin_number:

                if Card.objects.filter(card_number=receiver_card_number).exists(): 

                    # gets receiver's balance based on receiver's card number
                    receiver_card_balance = Card.objects.get(card_number=receiver_card_number).balance
                    # get receiver's card name
                    receiver_card_name = Card.objects.get(card_number=receiver_card_number).card_name
                    
                    if int(amount) <= user_balance:
                        # performs transfer 
                        user_balance -= int(amount)
                        receiver_card_balance += int(amount)

                        # perform database updates for user and receiver cards
                        Card.objects.get(card_number=receiver_card_number).save()
                        Card.objects.get(card_number=user_card_number).save()

                        messages.success(request, 'Transfer Success! ' + '$'+ amount + ' has been transferred from card: ' + user_card_name + ' to card: ' + receiver_card_name)       
                    else:
                        messages.error(request, 'Insufficient Balance')
                else:
                    messages.error(request, 'Receiver\'s Card Number is incorrect') 
            else:
                    messages.error(request, 'Your Pin is incorrect')    
        else:
            messages.error(request, 'Your Card Number or Pin is incorrect')

    return render(request, 'transfer.html')

def admin_log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        account = authenticate(request, username = username, password = password)
        # if account is valid, logs it in
        if account is not None:
            login(request, account)
            messages.success(request, 'Login Success!')
            return redirect('/admin-account-panel')
        else:
            messages.error(request, 'Username OR Password is incorrect')

    return render(request,'admin-login.html')

def admin_log_out(request):
	logout(request)
	return redirect('/admin-login')

@login_required(login_url='/admin-login')
def admin_account_panel(request):
    card = Card.objects.all()
    account = Account.objects.all()

    context = {'card': card, 'account':account}
    return render(request, 'admin-account-panel.html', context)

@login_required(login_url='login')
def card_details(request):
    card_name = request.GET.get('card_name')
    card = Card.objects.filter(card_name=card_name)
    context = {'card': card}
    return render(request, 'card-details.html', context)

def account_details(request):
    account_name = request.GET.get('account_name')
    account = Account.objects.filter(account_name=account_name)
    context = {'account': account}
    return render(request, 'account-details.html', context)

@login_required(login_url='login')
def atm_status(request):
    atm = ATM_Machine.objects.all();
    context = {'atm':atm}
    return render(request, 'atm-status.html', context)





