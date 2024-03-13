from django.contrib.auth.models import User
from django.shortcuts import render
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
            return JsonResponse({"error": "User already exists with this username"}, status=400)
        
        user = User.objects.create_user(
            username=username.lower(), email=email, password=password)
        
        if user is not None:
            return JsonResponse({"message": "User created successfully"})
        else:
            return JsonResponse({"error": "Failed to create user"}, status=500)

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not User.objects.filter(username=username).exists():
            return JsonResponse({"error": "User not found"}, status=404)

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            user_data = {
                'username': user.username,
                'email': user.email,
            }
            return JsonResponse({'message': "User logged in", 'userData': user_data})
        else:
            return JsonResponse({"error": "Invalid password"}, status=401)

    return JsonResponse({'error': "Method not allowed , use POST method"}, status=405)

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
    

