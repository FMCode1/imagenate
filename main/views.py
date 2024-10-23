from django.shortcuts import render
import os
from openai import OpenAI

client = OpenAI(api_key=api_key)
import requests
from dotenv import load_dotenv
from django.core.files.base import ContentFile
from .models import Image  # Make sure to import your Image model

# Load the API key from the environment variables
load_dotenv()
api_key = os.getenv('API_KEY', None)

def imagenate(request):
    img_obj = None  # Initialize the image object to None

    if api_key is not None and request.method == 'POST':  # If an API key exists and the user requests to post the form
        user_input = request.POST.get('user_input')  # Get the user input from the post request
        try:
            # Create an image using the prompt and size parameters
            response = client.images.generate(prompt=user_input,
            n=1,
            size='256x256')

            # Store the URL from the response
            img_url = response.data[0].url
            response = requests.get(img_url)  # Make a request to get the image content
            img_file = ContentFile(response.content)  # Create a content file using the image content

            fnum = Image.objects.count() + 1  # Set the file number
            fname = f'image-{fnum}.jpg'  # Set the file name

            # Create the image object and save the AI-generated image
            img_obj = Image(prompt=user_input)  # Adjust according to your model fields
            img_obj.ai_image.save(fname, img_file)  # Save the image in the database
            img_obj.save()  # Save the image object in the database

            print(img_obj)

        except Exception as e:
            print(f"Error generating image: {e}")

    return render(request, 'main/main.html', {'image_object': img_obj})  # Render the main.html template with the image object