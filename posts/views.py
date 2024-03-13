import tempfile
import os
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt 
from django.contrib.auth.decorators import login_required
from .models import *
from .utils import cloudinary
from django.shortcuts import get_object_or_404


@csrf_exempt
@login_required
def create_post(request):
    if request.method == 'POST':
        image = request.FILES.get('image')

        if not image:
            return JsonResponse({'error': 'Please provide an image and caption'})
        
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(image.read())
            tmp_file.flush()
            tmp_file_path = tmp_file.name

        try:
            image_url = cloudinary.upload_image(tmp_file_path)
        finally:
            os.remove(tmp_file_path)
        
        post = ImagePost.objects.create(
            file_url=image_url, user=request.user)
        
        # userPost = {
        #     'id': post.id,
        #     'image': post.image,
        #     'caption': post.caption,
        # }

        return redirect('/posts/all-post/')
    
    return render(request, 'create_post.html')
    

@csrf_exempt
@login_required
def get_all_post(request):
    if request.method == 'GET':
        user = request.user
        posts = ImagePost.objects.filter(user=user.id)
        data = []
        for post in posts:
            data.append({
                'id': post.id,
                'file': post.file_url,
            })
            print(data)
        return render(request, 'dashboard.html', context={'data':data})



@csrf_exempt
@login_required
def delete_post(request):
    if request.method == 'DELETE':
        post_id = request.GET.get('post_id')
        print(post_id)
        if not post_id:
            return JsonResponse({'error': 'Please provide a post ID'})
        
        post = ImagePost.objects.get(id=post_id, user=request.user)
        cloudinary.delete_post(post.image)
        post.delete()
        return JsonResponse({'success': True})
    
    return JsonResponse({'error': 'Invalid request method'})



