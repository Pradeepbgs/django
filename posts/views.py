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
        caption = request.POST.get('caption')

        if not image or not caption:
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
            image=image_url, caption=caption, user=request.user)
        
        userPost = {
            'id': post.id,
            'image': post.image,
            'caption': post.caption,
        }

        return JsonResponse({'success': True, 'data':{'post':userPost}})
    
    return JsonResponse({'error': 'Invalid request method', 'data':{}})
    

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
                'image': post.image.url,
                'caption': post.caption
            })
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



@csrf_exempt
@login_required
def comment_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        comment_text = request.POST.get('comment')

        if not post_id or not comment_text:
            return JsonResponse({'error': 'Please provide a post ID and comment'})

        try:
            post = ImagePost.objects.get(id=post_id)
        except ImagePost.DoesNotExist:
            return JsonResponse({'error': 'Post not found'})

        Comment.objects.create(post=post, user=request.user, comment=comment_text)

        return JsonResponse({'success': True})

    return JsonResponse({'error': 'Invalid request method'})

@csrf_exempt
@login_required
def toggle_like_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')

        if not post_id:
            return JsonResponse({'error': 'Please provide a post ID'})

        post = get_object_or_404(ImagePost, id=post_id)
        like, created = Like.objects.get_or_create(post=post, likedBy=request.user)

        if not created:
            like.delete()
            liked = False
        else:
            liked = True

        return JsonResponse({'success': True, 'liked': liked})


    return JsonResponse({'error': 'Invalid request method'})


@csrf_exempt
@login_required
def toggle_like_comment(request):

    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')

        if not comment_id:
            return JsonResponse({'error':'Please Provide a Comment_id'})
        
        comment = get_object_or_404(Comment, id=comment_id)

        if not comment:
            return JsonResponse({'error':'No Comments Found!'})
        
        like, created = Like.objects.get_or_create(comment=comment, likedBy=request.user)
        if not created:
            like.delete()
            liked = False
        else:
            liked = True

        return JsonResponse({'success':True,'liked':liked})
    
    return JsonResponse({'error':'Invalid Request Method'})
        
