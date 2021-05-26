from django.shortcuts import redirect, render
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    request.session.flush()
    return render(request, 'index.html')

def success(request):
    if "user_id" not in request.session:
        return redirect('/')
    this_user = User.objects.filter(id = request.session['user_id'])
    context = {
        'user': this_user[0],
        'wall_messages': Wall_Message.objects.all()
    }
    return render(request, 'success.html', context)

def register(request):
    if request.method == 'POST':
        errors = User.objects.validate_reg(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')

        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()

        new_user = User.objects.create(
            first_name = request.POST['first_name'], 
            last_name = request.POST['last_name'], 
            email = request.POST['email'], 
            password = hashed_pw
            )

        request.session['user_id'] = new_user.id
        return redirect('/success')
    return redirect('/')


def login(request):
    if request.method == 'POST':
        errors = User.objects.validate_login(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        this_user = User.objects.filter(email=request.POST['email'])
        request.session['user_id'] = this_user[0].id
        return redirect('/success')
    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')

def post_message(request):
    message = request.POST['message']
    poster = User.objects.get(id=request.session['user_id'])
    Wall_Message.objects.create(message=message, poster=poster)
    return redirect('/success')

def add_comment(request, id):
    comment = request.POST['comment']
    poster = User.objects.get(id=request.session['user_id'])
    message = Wall_Message.objects.get(id=id)
    Comment.objects.create(comment=comment, poster=poster, wall_message=message)
    return redirect('/success')

def profile(request, id):
    context = {
        'user': User.objects.get(id=id)
    }
    return render(request, 'profile.html', context)

def add_like(request, id):
    message_liked = Wall_Message.objects.get(id=id)
    user_like = User.objects.get(id=request.session['user_id'])
    message_liked.likes.add(user_like)
    return redirect('/success')


