from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login

@csrf_exempt
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        existUser = User.objects.filter(username=username).exists()
        if existUser:
            return JsonResponse({"msg": "User already exists with this username"})
        
        user = User.objects.create_user(
            username=username.lower(), email=email, password=password)
        
        if user is not None:
            return JsonResponse({"msg": "User created successfully"})

        
@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not User.objects.filter(username=username).exists():
            return JsonResponse({"msg": "Can't find user"})

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            user_data = {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
            return JsonResponse({'user': "User logged in", 'userData': user_data})
        else:
            return JsonResponse({"msg": "Invalid password"})

    return JsonResponse({'msg': "Method not allowed"})
