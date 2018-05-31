from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model

from .forms import UserLoginForm, UserRegisterForm

# Create your views here.
def register_view(request):
    
    if request.user.is_authenticated:
        return redirect('/home') # Set to whatever home page will be
        
    form = UserRegisterForm(request.POST)
    title = 'Register'
    description = 'Please enter your details to register'
    context = {'form':form, 'title':title, 'description':description, 'register_page':True}
    
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)

        return redirect('/home') # Set to whatever home page will be

    return render(request, 'users/form.html', context)


def login_view(request):
    
    if request.user.is_authenticated:
        return redirect('/home') # Set to whatever home page will be

    form = UserLoginForm(request.POST)
    title = 'Login'
    description = 'Please login to view page content'
    context = {'form':form, 'title':title, 'description':description, 'login_page':True}
    
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)

        return redirect('/home') # Set to whatever home page will be
    
    return render(request, 'users/form.html', context)


def logout_view(request):
    logout(request)
    return redirect('/home') # Set to whatever home page will be