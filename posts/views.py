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