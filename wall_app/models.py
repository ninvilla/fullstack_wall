from django.db import models
import re
import bcrypt


class UserManager(models.Manager):
    def validate_reg(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters"

        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters"

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['email']) == 0:
            errors['email'] = "Email must be entered"
        elif not EMAIL_REGEX.match(postData['email']):           
            errors['email'] = "Invalid email address"

        current_users = User.objects.filter(email=postData['email'])
        if len(current_users) > 0:
            errors['duplicate'] = "Email is already in use"

        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        if postData['password'] != postData['confirm_password']:
            errors['mismatch'] = "Passwords do not match"
        
        return errors


    def validate_login(self, postData):
        errors = {}
        existing_user = User.objects.filter(email=postData['email'])
        if len(existing_user) != 1:
            errors['email'] = "User does not exist."
        if len(postData['email']) == 0:
            errors['email'] = "Email must be entered"

        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        
        elif bcrypt.checkpw(postData['password'].encode(), existing_user[0].password.encode()) != True:
            errors['mismatch'] = "Email and password do not match"
        return errors



class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Wall_Message(models.Model):
    message = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name="user_messages", on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='liked_posts')


class Comment(models.Model):
    comment = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name='user_comments', on_delete=models.CASCADE)
    wall_message = models.ForeignKey(Wall_Message, related_name="post_comments", on_delete=models.CASCADE)

