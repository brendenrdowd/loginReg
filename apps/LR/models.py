# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core import validators #
from django.db import models #import objects from models library
import re #import regex for validations
import bcrypt #import password encrypter

class UserManager(models.Manager):
    def regVal(self,postData): #first function, make sure the function in views matches
        print "*********"
        print postData['email']
        print "*********"
        response = { #building the response
            'status' : True,
            'errors' : []
            }
        EMAIL_regex = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
        if not postData['fname'].isalpha() or not postData['lname'].isalpha():
            response["errors"].append("Names cannot contain numbers")
        if len(postData["fname"]) < 2:
            response["errors"].append("First name must be at least two characters!")
        if len(postData["lname"]) < 2:
            response["errors"].append("Last name must be at least two characters!")
        if not re.match(EMAIL_regex, postData['email']):
            response["errors"].append("Not a valid email!")
        if postData['password'] == None or len(postData["password"]) < 8:
            print 'password fails'
            response["errors"].append("Password must be at least 8 characters!")
        if postData["password"] != postData["confirm"]:
            response["errors"].append("Passwords do not match!")
        emailObject = self.filter(email = postData["email"])
        if len(emailObject) > 0:
            response["errors"].append("Email is already in database!")
        if len(response["errors"]) == 0:
            hashed = bcrypt.hashpw((postData['password'].encode()), bcrypt.gensalt(12))
            user = self.create(fname = postData["fname"], lname = postData["lname"], email = postData["email"], password = hashed)
            response["user"] = user
            print user
            return response
        response["status"] = False
        return response

    def logVal(self,postData):
        response = {
            'status' : True,
            'errors' : []
            }
        try:
            user = self.get(email = postData["email"])
        except:
            user = None
        if not user:
            response["errors"].append("Email is not registered!")
        if user:
            if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                response["errors"].append("Password does not match registered email.")
        if len(response["errors"]) == 0:
            response["user"] = user
            return response
        response["status"] = False
        return response

class User(models.Model):
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __repr__(self):
        return "User: \n{}\n{}\n{}\n{}\n{}".format(self.id,self.fname,self.lname,self.email,self.password)
    def __str__(self):
        return "User: \n{}\n{}\n{}\n{}\n{}".format(self.id,self.fname,self.lname,self.email,self.password)
