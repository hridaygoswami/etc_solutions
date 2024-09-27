import os
import logging
from django.db import models
from django.core.exceptions import ValidationError
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.conf import settings

# Set up logging
logger = logging.getLogger(__name__)

# Category model for categorizing main content
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# MainContent model that contains the title, date, and description
class MainContent(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.TextField(default='Title')
    date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return f"{self.category} - {self.date}"

# Helper function to generate paths for original and resized images in the static folder
def upload_to(instance, filename, folder):
    main_content_id = instance.main_content.id
    existing_photos = instance.main_content.photos.all()

    # Increment photo count if photos already exist
    photo_count = existing_photos.count() + 1 if existing_photos.exists() else 1

    # Change extension to '.jpg' regardless of the original extension
    filename = f'{photo_count}.jpg'

    # Define the storage path in the static folder
    return f'website/static/{main_content_id}/{folder}/{filename}'

# Function to handle original image upload to the static folder
def upload_original_image(instance, filename):
    return upload_to(instance, filename, 'original')

# Photo model that stores original and resized images
class Photo(models.Model):
    main_content = models.ForeignKey(MainContent, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to=upload_original_image)  # Store in static folder as jpg
    resized_image = models.ImageField(upload_to=upload_original_image, blank=True, null=True)  # Resized image will also be jpg

    def __str__(self):
        return f"Photo for {self.main_content}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        # Log the image upload
        logger.info(f"Saving original image: {self.image.name}")

        try:
            img = Image.open(self.image)

            # Convert image to RGB (necessary for saving as JPG)
            if img.mode != 'RGB':
                img = img.convert('RGB')

            # Save the original image as .jpg
            original_thumb = BytesIO()
            img.save(original_thumb, format='JPEG')
            original_thumb.seek(0)

            # Overwrite the original image with the new JPG version
            self.image.save(
                upload_to(self, os.path.basename(self.image.name), 'original'),
                InMemoryUploadedFile(
                    original_thumb,
                    None,
                    f'{os.path.basename(self.image.name)}.jpg',  # Force jpg extension
                    'image/jpeg',  # Set the content type to jpeg
                    original_thumb.tell(),
                    None
                ),
                save=False
            )

            # Resize the image to 350x350 pixels if necessary
            if img.width != 350 or img.height != 350:
                img = img.resize((350, 350), Image.LANCZOS)

                # Save the resized image to an in-memory file
                temp_thumb = BytesIO()

                # Save the resized image as .jpg
                img.save(temp_thumb, format='JPEG')
                temp_thumb.seek(0)

                # Save the resized image to the static folder
                self.resized_image.save(
                    upload_to(self, os.path.basename(self.image.name), 'resized'),
                    InMemoryUploadedFile(
                        temp_thumb,
                        None,
                        f'{os.path.basename(self.image.name)}.jpg',  # Force jpg extension
                        'image/jpeg',  # Set the content type to jpeg
                        temp_thumb.tell(),
                        None
                    ),
                    save=False
                )

            logger.info(f"Successfully saved resized image: {self.resized_image.name}")

        except Exception as e:
            logger.error(f"Error processing image: {e}")

# Signal to delete images from the static folder when the Photo instance is deleted
@receiver(post_delete, sender=Photo)
def delete_photo_from_static(sender, instance, **kwargs):
    # Delete the original and resized images from the static folder
    if instance.image and os.path.exists(instance.image.path):
        os.remove(instance.image.path)
    if instance.resized_image and os.path.exists(instance.resized_image.path):
        os.remove(instance.resized_image.path)
