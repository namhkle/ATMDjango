from django.contrib import admin
from ATM.models import*

# Register your models here.

class AccountColumns(admin.ModelAdmin):
    list_display = ('account_name','account_number','password','phone_number')

class CardColumns(admin.ModelAdmin):
    list_display = ('card_name','card_number', 'balance', 'issue_date', 'exp_date')

class ATMmachineColumns(admin.ModelAdmin):
    list_display = ('status', 'balance', 'last_refill', 'next_refill')

admin.site.register(Account, AccountColumns)
admin.site.register(Card,CardColumns)
admin.site.register(ATM_Machine,ATMmachineColumns)