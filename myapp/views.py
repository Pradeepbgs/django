from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login

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

    return JsonResponse({'error': "Method not allowed"}, status=405)
