import tempfile
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt 
from django.contrib.auth.decorators import login_required
from .models import *
from .utils import cloudinary


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

        return JsonResponse({'data': data})

    return JsonResponse({'error': 'Invalid request method'})


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


def toggle_like_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')

        if not post_id:
            return JsonResponse({'error': 'Please provide a post ID'})

        Like.objects.filter(post=post_id, user=request.user)

        return JsonResponse({'success': True})

    return JsonResponse({'error': 'Invalid request method'})