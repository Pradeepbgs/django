# Import the required libraries
import os
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
import cloudinary.api

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

def upload_image(image):
    upload_result = cloudinary.uploader.upload(image)
    return upload_result.get('secure_url')


def delete_post(image_url):
    public_id = image_url.split("/").pop().split(".")[0]
    return cloudinary.uploader.destroy(public_id)