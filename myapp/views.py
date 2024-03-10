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
            return JsonResponse({"msg":"user already exists with this username"})
        hashed_password = make_password(password)
        print(hashed_password)
        user = User.objects.create_user(
            username=username.lower(),email=email,password=hashed_password)

        if user is not None:
            return JsonResponse({"msg":"user created successfully"})
        
@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return JsonResponse({'user':"user logged in",'userData':user})
        else:
            return JsonResponse({"msg":"cant find user"})

    return JsonResponse({'msg':"cant find"})