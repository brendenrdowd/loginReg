# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect,HttpResponse
from django.core.urlresolvers import reverse
from .models import *
from django.contrib import messages
import bcrypt

#NEED TO:
#GIVE SEPERATE MESSAGES FOR LOGIN AND REGISTRATION ERRORS
#IF NOT ALREADY, COMPARE LOGIN EMAIL TO DATABASE
#COMPARE REGISTRATION AGAINST DATABASE TO PREVENT DUPLICATE ENTRIES
#GRAB LOGIN ID IN SESSION FOR SUCCESS PAGE REFERENCE

def index(request):
    return render(request,'LR/index.html')

def register(request):
    result = User.objects.regVal(request.POST) #make sure this matches on models.py
    if result['status'] == False:
        for err in result['errors']:
            messages.error(request, err)
            return redirect('/')
    else:
        password = request.POST['password']
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        request.session['user_id'] = result['user'].id
        print User.objects.all()
        return redirect('/success')

def login(request):
    password = request.POST['password']
    hashed = bcrypt.haspw(password.encode(), bcrypt.gensalt())
    #check if they exist against what I have in the database?
    try: #don't understand this part
        user = User.objects.get(email = email)
        hash1 = user.password
    except:
        hash1 = request.POST['email']
    result = User.objects.logVal(request.POST) #make sure this matches on models.py
    if result['status'] == False:
        for err in result['errors']:
            messages.error(request, err)
        return redirect('/')
    else:
        request.session['user_id'] = result['user'].id
        return redirect('/success')

def success(request):
    try:
        request.session['user_id']
    except KeyError:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request,'LR/success.html',context)
