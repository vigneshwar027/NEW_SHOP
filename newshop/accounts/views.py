from django.http import request
from django.shortcuts import render , redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages

from .models import *

# Create your views here.
 

def register(request):

    if request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']


        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username taken')
                return redirect('reg')    

            elif User.objects.filter(email=email).exists():
                messages.info(request,'Mail ID taken')
                return redirect('reg')    

            else:   
                user = User.objects.create_user(username=username,first_name=firstname, last_name=lastname, password=password1, email = email)
                user.save();
                #remember the above two line code for user creation
                # User.xxxx (U should be capital and it is objects not object)
                # print('user created')
                      
        else:
            # print('PASSWORD NOT MATCHING')    
            messages.info(request,'PASSWORD NOT MATCHING')    
            return redirect('reg')    
        return redirect('/')    

    else:
        return render(request,'register.html')
        

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password'] 

        id = auth.authenticate(username=username,password=password)

        if id is not None: #its None not none
            auth.login(request,id) #for logging in process
            return redirect('/')
        else:
            messages.info(request,'invalid credentials')
            return redirect('login')
         
    else:
        return render(request,'login.html',{'code':'hello'})
    
def logout(request):
    auth.logout(request)
    return redirect('/')




  


