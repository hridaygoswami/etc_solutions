from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.dispatch import receiver
from PIL import Image
import os

# Define the Category model without predefined choices
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# Define the MainContent model
class MainContent(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.TextField(default='Title')
    date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return f"{self.category} - {self.date}"

# Function to determine the upload path for original and resized images
def upload_to(instance, filename, folder):
    main_content_id = instance.main_content.id
    photo_count = instance.main_content.photos.count() + 1
    filename = f'{photo_count}{os.path.splitext(filename)[1]}'
    return f'photos/{main_content_id}/{folder}/{filename}'

# Named function to be used for the upload_to argument
def upload_original_image(instance, filename):
    return upload_to(instance, filename, 'original')

# Define a separate model for handling photos
class Photo(models.Model):
    main_content = models.ForeignKey(MainContent, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to=upload_original_image)

    def __str__(self):
        return f"Photo for {self.main_content}"

    class Meta:
        unique_together = ['main_content', 'image']

    def save(self, *args, **kwargs):
        # Save the original image first
        super().save(*args, **kwargs)

        # Open the original image using Pillow
        original_img = Image.open(self.image.path)

        # Create a new path for the resized image
        resized_path = upload_to(self, os.path.basename(self.image.path), 'resized')
        resized_full_path = os.path.join(os.path.dirname(self.image.path), resized_path)

        # Ensure the directory for resized images exists
        os.makedirs(os.path.dirname(resized_full_path), exist_ok=True)

        # Resize the image to 350x350 pixels
        if original_img.width != 350 or original_img.height != 350:
            resized_img = original_img.resize((350, 350), Image.Resampling.LANCZOS)
            resized_img.save(resized_full_path)

# Validate photo limit
@receiver(pre_save, sender=Photo)
def validate_photo_limit(sender, instance, **kwargs):
    if instance.main_content.photos.count() >= 10:
        raise ValidationError("You can only upload up to 10 photos.")
