from django.db import models
from django import forms
from datetime import datetime, timedelta
from sys import *
import random

# Create your models here.
# Makes a database for each model


class Account(models.Model):
    account_number = models.PositiveIntegerField(primary_key=True) 
    account_name = models.CharField(max_length=30)
    phone_number = models.PositiveIntegerField()   

    def __str__(self):
        return self.account_name

class Card(models.Model):
    card_number = models.PositiveIntegerField(primary_key=True) 
    '''account_number = models.ForeignKey(Account, to_field='account_number',
                                default=Account.account_number, on_delete=models.CASCADE)'''
    pin = models.PositiveIntegerField(default=False)                             
    card_name = models.CharField(max_length=30)
    issue_date = models.DateField()
    exp_date = models.DateField(default=datetime.now() + timedelta(days=1095))
    balance = models.PositiveIntegerField() 
    address = models.CharField(max_length=60)  
    phone_number = models.PositiveIntegerField()

    def __str__(self):
        return self.card_name
 
class ATM_Machine(models.Model):
    atm_uid = models.PositiveIntegerField(primary_key=True)
    balance = models.PositiveIntegerField()
    min_enquiry = models.PositiveIntegerField()
    last_refill = models.DateField()
    next_refill = models.DateField()

    def __str__(self):
        return str(self.atm_uid)






