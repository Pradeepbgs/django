from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt 
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password

def get_home_page(request):
    return render(request, 'index.html')

@csrf_exempt
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "User already exists with this username")
            return render(request, 'register.html')

        user = User.objects.create_user(
            username=username.lower(), email=email, password=password)

        if user is not None:
            messages.success(request, "User created successfully")
            return redirect('login')
        else:
            messages.error(request, "Failed to create user")
            return render(request, 'register.html')

    return render(request, 'register.html')


@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not User.objects.filter(username=username).exists():
            messages.error(request, "User not found")
            return render(request, 'login.html')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            user_data = {
                'username': user.username,
                'email': user.email,
            }
            return redirect('/posts/all-post/')
        else:
            messages.error(request, "Invalid password")
            return render(request, 'login.html')

    return render(request, 'login.html')

@csrf_exempt
@login_required 
def user_logout(request):
    if request.method == "POST":
        logout(request)
        return JsonResponse({'msg':'you are logged out '})
    else:
        JsonResponse({'msg':'method is not allowed , use post method'})


@csrf_exempt
@login_required
def change_user_deatils(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = request.user

        if username:
            User.objects.filter(username=user.username).update(username=username)
            
        if password:
            user.password = make_password(password)
            
        user.save()

        return JsonResponse({'msg': 'user details updated'})
    else:
        return JsonResponse({'msg': 'method is not allowed, use post method'})
    

