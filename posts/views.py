from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt 
from django.contrib.auth.decorators import login_required
from .models import *


@csrf_exempt
@login_required
def create_post(request):
    
    if request.method == 'POST':
        image = request.FILES.get('image')
        caption = request.POST.get('caption')

        if not image or not caption:
            return JsonResponse({'error': 'Please provide an image and caption'})
        
        post = ImagePost(image=image, caption=caption)
        post.save()

        return JsonResponse({'success': True})
    
    return JsonResponse({'error': 'Invalid request method'})
    

@csrf_exempt
@login_required
def get_all_post(request):

    if request.method == 'GET':
        posts = ImagePost.objects.all()
        data = []
        for post in posts:
            data.append({
                'id': post.id,
                'image': post.image.url,
                'caption': post.caption
            })

        return JsonResponse({'data': data})

    return JsonResponse({'error': 'Invalid request method'})