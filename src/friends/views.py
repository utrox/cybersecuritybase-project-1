from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse

from .models import Secret


User = get_user_model()


@login_required
def index(request):
    friends = request.user.friends.all()
    return render(request, 'friends/index.html', {'friends': [f.username for f in friends]})


@login_required
def add_friend(request):
    if request.method == 'POST':
        # FIX FOR PROBLEM #1 - A1: SQL Injection 
        # Easiest is to just use the ORM way to get the user object
        # try:
        #   friend = User.objects.get(id=request.POST['username'])
        # except User.DoesNotExist:
        #   return HttpResponse('User not found', status=404)
        result = User.objects.raw(f"SELECT * FROM friends_user WHERE username = '{request.POST['username']}'")
        if len(result) == 0:
            return HttpResponse('User not found', status=404)
        
        request.user.friends.add(result[0])
        return redirect('/')
    return render(request, 'friends/add.html')


def user_owns_secret_wrapper(fn):
    def wrapper(request, *args, **kwargs):
        secret_id = kwargs.get('secret_id')
        try:
            secret = Secret.objects.get(id=secret_id)
            if secret.user == request.user:
                return fn(request, *args, **kwargs)
        except Secret.DoesNotExist:
            pass
        return HttpResponse('Unauthorized', status=401)
    return wrapper

# FIX FOR PROBLEM #4 - A5:2017 Broken Access Control
# This is a simple example of how to fix the problem of broken access control.
# We don't want other users to be able to see the some data of other users.
# So we can use a decorator to check if the user is the owner of the secret.
# @user_owns_secret_wrapper
def get_secrets(request, secret_id):
    try:
        secret = Secret.objects.get(id=secret_id)
    except Secret.DoesNotExist:
        return HttpResponse('Secret not found', status=404)
    return render(request, 'friends/secret.html', {'secret': secret.secret_data})


def add_secrets(request):
    if request.method == 'POST':
        secret = Secret(user=request.user, secret_data=request.POST['secret_data'])
        secret.save()
        return redirect(f'/api/secrets/{secret.id}/')
    return render(request, 'friends/add_secret.html')