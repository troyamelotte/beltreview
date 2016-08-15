from __future__ import unicode_literals

from django.db import models
import re
import bcrypt
EMAILCHECK = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.
class UserManager(models.Manager):
    def checkreg(self, first, last, alias, email, password, confirm_password):
        errorlist = []
        count = 0
        if len(first)<2:
            errorlist.append('First name too short!')
            count +=1

        if len(last)<2:
            errorlist.append('Last name too short!')
            count+=1

        if len(alias)<4:
            errorlist.append('Alias too short!')
            count+=1
        elif User.objects.filter(alias=alias).exists():
            errorlist.append('Alias taken')
            count+=1

        if len(email)<1:
            errorlist.append('Email is required!')
            count+=1
        elif User.objects.filter(email=email).exists():
            count+=1
            errorlist.append('email exists!')

        elif not EMAILCHECK.match(email):
            errorlist.append('Please enter a valid email!')
            count+=1

        if not password==confirm_password:
            errorlist.append('Passwords are not the same!')
            count+=1
        elif len(password)<8:
            errorlist.append('Please enter a password longer than 8 characters!')
            count+=1

        if count==0:
            return True
        return errorlist

    def checklog(self, email, password):
        errorlist = []
        count = 0
        user = User.objects.get(email=email)
        print(user)
        print('*'*50)
        password=password.encode()
        if not email == user.email:
            count+=1
            errorlist.append('Email incorrect')
        if bcrypt.hashpw(password, bcrypt.gensalt()) == user.password:
            count+=1
            errorlist.append('Password incorrect')

        if count == 0:
            return [True, user]
        return errorlist

class User(models.Model):
    first = models.CharField(max_length=30)
    last = models.CharField(max_length=30)
    alias = models.CharField(max_length=30)
    email = models.EmailField()
    password = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    userManager = UserManager()
    objects = models.Manager()

class BookManager(models.Manager):
    def bookchecker(self, title,review, author = 'None' ):
        errorlist = []
        count=0
        if len(title)<1:
            count+=1
            errorlist.append('Please enter a title')
        if Author.objects.filter(name=author).exists():
            count+=1
            errorlist.append('Author already exists! Please select it from the dropdown')
        if len(review)<20:
            count+=1
            errorlist.append('Reviews must be at least 20 characters!')
        if count == 0:
            return True
        else:
            return errorlist

class ReviewManager(models.Manager):
    def reviewchecker(self, review):
        errorlist = []
        count=0
        if len(review)<20:
            errorlist.append('Reviews must be at least 20 characters')
            count+=1
        if count ==0:
            return True
        else:
            return errorlist

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey('Author', related_name="BookToAuthor")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    bookManager = BookManager()
    objects= models.Manager()

class Author(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Review(models.Model):
    review = models.TextField(max_length=1000)
    rating = models.TextField(max_length=2)
    user = models.ForeignKey('User', related_name="ReviewToUser")
    Book = models.ForeignKey('Book', related_name="ReviewToBook")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    reviewManager = ReviewManager()
    objects = models.Manager()
