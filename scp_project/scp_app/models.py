from django.db import models
from datetime import datetime
import re

name_regex = re.compile(r'^[a-zA-Z. -]+$')
# title_regex = re.compile(r'^[a-zA-Z0-9,: -]+$')
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
pw_regex = re.compile(r'^[a-zA-Z0-9.!@#$%^&*() -]+$')

# Create your models here.
class UserManager(models.Manager):
    def user_validator(self, postData):
        errors = {}
        if len(postData["username"]) < 2:
            errors["username_short"] = "Not enough characters or blank for Username"
        else:
            if not name_regex.match(postData["username"]):
                errors["invalid_username"] = "Invalid characters in Username"
        if not email_regex.match(postData["email"]):
            errors["invalid_email"] = "Invalid email was entered"
        if len(postData["password"]) < 8:
            errors["short_pw"] = "Password needs to be at least 8 Characters"
        else:
            if not pw_regex.match(postData["password"]):
                errors["invalid_pw"] = "Invalid characters in password"
            if postData["password"] != postData["conf_password"]:
                errors["pw_match"] = "Password doesn't match"
        return errors

    def email_validator(self, postData):
        errors = {}
        if not email_regex.match(postData["email"]):
            errors["invalid_email"] = "Invalid email was entered"
        if len(postData["password"]) < 8:
            errors["short_pw"] = "Password needs to be at least 8 Characters"
        if not User.objects.filter(email=postData["email"]):
            errors["invalid_user"] = "Unauthorized User"
        return errors

class EventManager(models.Manager):
    def book_validator(self, postData):
        errors = {}
        if len(postData["title"]) < 2:
            errors["invalid_title"] = "Title too short or blank"
        if len(postData["desc"]) < 5:
            errors["short_desc"] = "Description too short or blank"
        # if not title_regex.match(postData["title"]):
        #     errors["invalid_title"] = "Invalid characters for title"
        return errors

class User(models.Model):
    username = models.CharField(max_length=45)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Event(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    created_by = models.ForeignKey(User, related_name="events", on_delete=models.CASCADE)
    users_rsvp = models.ManyToManyField(User,related_name="rsvp")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = EventManager()
