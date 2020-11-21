from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime, timedelta
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

            #need to actually create the object to update its values
            userCardObject = Card.objects.get(card_number=user_card_number) #*important*
            if int(user_pin) == userCardObject.pin:
                if userCardObject.status == 'Active':
                    if (int(amount) >= 10):
                        # performs deposit
                        userCardObject.balance += int(amount)
                        # updates transaction history
                        ts = datetime.now()
                        userCardObject.transaction_history += 'Deposit: + $' + amount + '          ' + str(ts) + '\n'
                        userCardObject.save()#*this is how it actually saves*     

                        # updates ATM machine balance
                        atmMachineObject = ATM_Machine.objects.get()
                        atmMachineObject.balance += int(amount)

                        atmMachineObject.save()       

                        messages.success(request, 'Deposit Success! ' + '$'+ amount + ' has been depositted from card: ' + userCardObject.card_name)   
                    else:
                        messages.error(request, 'Minimum deposit is $10')   
                else:
                    messages.error(request, 'Your card is currently inactive')
            else:
                messages.error(request, 'Your Pin is inccorect')
        else:
            messages.error(request, 'Your Card Number is incorrect')
    return render(request, 'deposit.html')


def withdrawal(request):
    if request.method == 'POST':
        user_pin = request.POST.get('Pin')
        user_card_number = request.POST.get('Your Card Number')      # gets user input for card number
        amount = request.POST.get('Amount')                          # gets user input for amount
    
        # Cash withdrawal: Validatation - checks if card number and pin exist and verify user's balance 
        if Card.objects.filter(card_number=user_card_number).exists(): 

            #need to actually create the object to update its values
            userCardObject = Card.objects.get(card_number=user_card_number) #*important*

            if int(user_pin) == userCardObject.pin:
                if userCardObject.status == 'Active':
                    if int(amount) <= userCardObject.balance:
                        if (int(amount) >= 10):
                            # performs withdrawal
                            userCardObject.balance -= int(amount)
                            # updates transaction history
                            ts = datetime.now()
                            userCardObject.transaction_history += 'Withdrawal: - $' + amount + '          ' + str(ts) + '\n'
                            userCardObject.save()#*this is how it actually saves* 

                            # updates ATM machine balance
                            atmMachineObject = ATM_Machine.objects.get()
                            atmMachineObject.balance -= int(amount)
                            atmMachineObject.save()    

                            messages.success(request, 'Withdrawal Success! ' + '$'+ amount + ' has been withdrawn from card: ' + userCardObject.card_name)   
                        else:
                            messages.error(request, 'Minimum withdrawal is $10')   
                    else:
                        messages.error(request, 'Insufficient Balance')
                else:
                    messages.error(request, 'Your card is currently inactive')
            else:
                messages.error(request, 'Your Pin is inccorect')
        else:
            messages.error(request, 'Your Card Number is incorrect')

    return render(request, 'withdrawal.html')

def transfer(request):
    if request.method == 'POST':   
        user_pin = request.POST.get('Pin')
        user_card_number = request.POST.get('Your Card Number')      # gets user input for card number
        amount = request.POST.get('Amount')                          # gets user input for amount

        # Transfer Validation - checks if user's and receiver's card number exist and verify user pin & balance 
        if Card.objects.filter(card_number=user_card_number).exists():
            userCardObject = Card.objects.get(card_number=user_card_number) #*important*

            # get receiver's account based on user input
            receiver_card_number = request.POST.get('Receiver Card number') 

            if int(user_pin) == userCardObject.pin:
                if Card.objects.filter(card_number=receiver_card_number).exists(): 

                    receiverCardObject = Card.objects.get(card_number=receiver_card_number) #*important*
                    
                    if userCardObject.status and receiverCardObject.status == 'Active':
                        if int(amount) <= userCardObject.balance:
                            if (int(amount) >= 10):
                                # performs transfer 
                                userCardObject.balance      -= int(amount)
                                receiverCardObject.balance  += int(amount)

                                # updates transaction history
                                ts = datetime.now()
                                userCardObject.transaction_history += 'Transfer: - $' + amount + '          ' + str(ts) + '\n'
                                userCardObject.save()       #*this is how it actually saves*
                                receiverCardObject.save()   #*this is how it actually saves*    
                                messages.success(request, 'Transfer Success! ' + '$'+ amount + ' has been transferred from card: ' + userCardObject.card_name + ' to card: ' + receiverCardObject.card_name)       
                            else:
                                messages.error(request, 'Minimum withdrawal is $10')   
                        else:
                            messages.error(request, 'Insufficient Balance')
                    else:
                        messages.error(request, 'Your card or receiver\'s card is currently inactive') 
                else:
                    messages.error(request, 'Receiver\'s Card Number is incorrect') 
            else:
                    messages.error(request, 'Your Pin is incorrect')    
        else:
            messages.error(request, 'Your Card Number or Pin is incorrect')

    return render(request, 'transfer.html')

def block_card(request):
    if request.method == 'POST':
        user_pin = request.POST.get('Pin')
        user_card_number = request.POST.get('Your Card Number')      # gets user input for card number
    
        # Card block: Validatation - checks if card number and pin exist
        if Card.objects.filter(card_number=user_card_number).exists(): 

            #need to actually create the object to update its values
            userCardObject = Card.objects.get(card_number=user_card_number) #*important*

            if int(user_pin) == userCardObject.pin:
                if userCardObject.status == 'Active':
                    # performs blocking
                    userCardObject.status = 'Inactive'
                    userCardObject.save()#*this is how it actually saves*    

                    messages.success(request, 'The following card has been block: ' + userCardObject.card_name)   
                else:
                    messages.error(request, 'Card' + userCardObject.card_name + ' is already Blocked/Inactive')
            else:
                messages.error(request, 'Your Pin is incorrect') 
        else:
            messages.error(request, 'Card Number is incorrect')

    return render(request, 'block-card.html')

def activate_card(request):
    if request.method == 'POST':
        user_pin = request.POST.get('Pin')
        user_card_number = request.POST.get('Your Card Number')      # gets user input for card number
    
        # Card activation: Validatation - checks if card number and pin exist 
        if Card.objects.filter(card_number=user_card_number).exists(): 

            #need to actually create the object to update its values
            userCardObject = Card.objects.get(card_number=user_card_number) #*important*

            if int(user_pin) == userCardObject.pin:
                if userCardObject.status == 'Active':
                    # performs blocking
                    userCardObject.status = 'Active'
                    userCardObject.save()#*this is how it actually saves*    

                    messages.success(request, 'The following card has been activated: ' + userCardObject.card_name)   
                else:
                    messages.error(request, 'Card' + userCardObject.card_name + ' is already Unblocked/Active')
            else:
                messages.error(request, 'Your Pin is incorrect') 
        else:
            messages.error(request, 'Your Card Number is incorrect')

    return render(request, 'activate-card.html')


def reset_pin(request):
    if request.method == 'POST':
        user_pin = request.POST.get('Pin')
        user_card_number = request.POST.get('Your Card Number')      # gets user input for card number
    
        # Card activation: Validatation - checks if card number and pin exist 
        if Card.objects.filter(card_number=user_card_number).exists(): 

            #need to actually create the object to update its values
            userCardObject = Card.objects.get(card_number=user_card_number) #*important*

            if userCardObject.status == 'Active':
                # performs pin reset
                userCardObject.pin = user_pin
                userCardObject.save()#*this is how it actually saves*    

                messages.success(request, 'Pin has been reset for the following card: ' + userCardObject.card_name)   
            else:
                messages.error(request, 'Card' + userCardObject.card_name + ' is currently blocked/inactive')
        else:
            messages.error(request, 'Your Card Number is incorrect')

    return render(request, 'reset-pin.html')

def update_phone(request):
    if request.method == 'POST':
        user_phone = request.POST.get('Phone')
        user_card_number = request.POST.get('Your Card Number')      # gets user input for card number
    
        # Card activation: Validatation - checks if card number and pin exist 
        if Card.objects.filter(card_number=user_card_number).exists(): 

            #need to actually create the object to update its values
            userCardObject = Card.objects.get(card_number=user_card_number) #*important*

            # performs phone number update
            userCardObject.phone_number = user_phone
            userCardObject.save()#*this is how it actually saves*  

            messages.success(request, 'Phone number has been updated for the following card: ' + userCardObject.card_name)   
        else:
            messages.error(request, 'Your Card Number is incorrect')

    return render(request, 'update-phone.html')


def view_history(request):
    context = {}
    if request.method == 'POST':
        user_card_number = request.POST.get('Your Card Number')      # gets user input for card number
    
        # Card activation: Validatation - checks if card number and pin exist 
        if Card.objects.filter(card_number=user_card_number).exists(): 

            #need to actually create the object to update its values
            userCardObject = Card.objects.get(card_number=user_card_number) #*important*

            transaction_history = userCardObject.transaction_history

            if transaction_history != '':
                context = {'transaction_history':transaction_history}

                messages.success(request, 'Transaction history has been generated for the following card: ' + userCardObject.card_name)   
            else: 
                messages.error(request, 'No History Found for the following card: ' + userCardObject.card_name )
        else:
            messages.error(request, 'Your Card Number is incorrect')

    return render(request,'view-history.html', context)

def update_expd(request):
    if request.method == 'POST':
        user_expd = request.POST.get('exp_date')
        user_card_number = request.POST.get('Your Card Number')      # gets user input for card number
    
        # Card activation: Validatation - checks if card number and pin exist 
        if Card.objects.filter(card_number=user_card_number).exists(): 

            #need to actually create the object to update its values
            userCardObject = Card.objects.get(card_number=user_card_number) #*important*

            # performs phone number update
            userCardObject.exp_date = user_expd
            userCardObject.save()#*this is how it actually saves*  
              
            messages.success(request, 'Expiration date has been updated for the following card: ' + userCardObject.card_name)   
        else:
            messages.error(request, 'Your Card Number is incorrect')

    return render(request, 'update-expd.html')

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





