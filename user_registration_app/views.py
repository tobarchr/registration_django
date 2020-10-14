from django.shortcuts import render, redirect
from django.contrib import messages
from user_registration_app.models import *
import bcrypt

def index(request):
    return render(request,'index.html')

def login(request):
    user = User.objects.filter(email=request.POST['email']) 
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(),logged_user.password.encode()):
            request.session['userid'] = logged_user.id
            return redirect ('/success')
    return redirect ('/')

def registration(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect ('/')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        User.objects.create(first_name = request.POST['reg_first_name'], last_name = request.POST['reg_last_name'], password = pw_hash, email=request.POST['email'])
        capture_user = User.objects.last()
        request.session['userid'] = capture_user.id
        return redirect('/success')

def success_screen(request):
    welcome_greeting = User.objects.get(id=request.session['userid'])
    context = {
        "user_info" : welcome_greeting
    }
    if 'userid'not in request.session:
        return redirect('/')
    else:
        return render(request,'welcome.html',context)

def logoff(request):
    del request.session['userid']
    return redirect ('/')