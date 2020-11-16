# ATMDjango

Login with  
username: admin   
pw: group1  
http://127.0.0.1:8000/admin/ 


You can add new accounts or use the existing accounts here in this module. You can see the password there. 1 of the 2 already created accounts is:
account name: tyler
pw: t
http://127.0.0.1:8000/admin/ATM/account/


Our homepage will be user login. 
http://127.0.0.1:8000/

We will go to this page after user login success
http://127.0.0.1:8000/user-account-panel/

This will be an example of card details if you click on one of the little card under "Your card(s)"
http://127.0.0.1:8000/user-account-panel/card-details/?card_name=miguel-card

These are the two features for user account, you can go there and test it out. They generally work but for some reason, save() currently does not work T.T. It does not update our database after withdrawl or transfer.  You can check out the two functions withdrawl & transfer in views.py and hope we solve the problem together. 
http://127.0.0.1:8000/user-account-panel/withdrawal/
http://127.0.0.1:8000/user-account-panel/transfer/

Plus, he wants us to transfer money from one account to another. Which is what we have not figured it out yet...it deals with foreignKey in the models.py file but let's figure it out together. 

If you want to go to admin account panel. Use this login page:
http://127.0.0.1:8000/admin-login/
Login with admin account 
username: admin 
pw: group1

Admin will be able to see all the  cards and accounts as well as the ATM machine status
http://127.0.0.1:8000/admin-account-panel/
http://127.0.0.1:8000/atm-status/

Feel free to add visual design to our project. 





