from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.




def anonymous_required(function=None, redirect_url=None):
    if not redirect_url:
        redirect_url = 'dashboard'

    actual_decorator = user_passes_test(
        lambda u: u.is_anonymous,
        login_url=redirect_url
    )

    if function:
        return actual_decorator(function)
    return actual_decorator


@anonymous_required
def login(request):

    if request.method=='POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user:
            auth.login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Username or password is incorrect!!!")
            return redirect('login')





    return render(request, 'authorization/login.html')

@anonymous_required
def register(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email'].replace(' ', '').lower()
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Password do not match!!!")
            return redirect('register')

        if User.objects.filter(email=email):
            messages.error(request, "User with that email already exists!!!")
            return redirect('register')
        
        if User.objects.filter(username=username):
            messages.error(request, "Username taken! Please try another one")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        auth.login(request, user)

        return redirect('dashboard')

        print(username + password1)
        

    return render(request, 'authorization/register.html')

@login_required
def logout(request):
    auth.logout(request)
    return redirect('login')

