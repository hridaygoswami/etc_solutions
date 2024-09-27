# import boto3
# from botocore.exceptions import NoCredentialsError

# s3 = boto3.client('s3')

# try:
#     s3.upload_file('test.txt', 'your-bucket-name', 'test/test.txt')
#     print("Upload successful")
# except FileNotFoundError:
#     print("The file was not found")
# except NoCredentialsError:
#     print("Credentials not available")


from django.test import TestCase
from .models import MainContent, Photo, Category
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

class PhotoModelTests(TestCase):
    def setUp(self):
        # Set up a category and main content for testing
        self.category = Category.objects.create(name="Test Category")
        self.main_content = MainContent.objects.create(
            category=self.category,
            title="Test Title",
            date="2024-09-25",
            description="Test description."
        )

    def test_photo_upload(self):
        # Create a dummy image
        image_file = SimpleUploadedFile(
            r"/Users/hridaygoswami/Downloads/Work/Personal/naitik/etc_website_content/new_proj/etc_solutions/Christmas Instagram Templates.jpeg",
            b"file_content",
            content_type="image/jpeg"
        )
        
        # Create the photo instance
        photo = Photo(main_content=self.main_content, image=image_file)
        
        # Save the photo instance
        photo.save()
        
        # Check if the photo was uploaded and resized
        self.assertTrue(photo.image.name.endswith('original/test_image.jpg'))
        self.assertTrue(photo.resized_image.name.endswith('resized/test_image.jpg'))

    def test_no_image_uploaded(self):
        # Test without uploading an image
        photo = Photo(main_content=self.main_content)
        
        # Save and check if the resized image is None
        photo.save()
        self.assertIsNone(photo.resized_image)
