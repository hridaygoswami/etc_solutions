from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import MainContent, Category, Photo
# Create your views here.
def index(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")

def gallery(request):
    category = Category.objects.all()
    content = []
    for i in category:
        content.append([i, MainContent.objects.filter(category=i)])
    content = dict(content)
    return render(request, "gallery.html", {
        "content": content,
    })

def gallery_indi(request, id):
    # Fetch the MainContent object with the provided ID
    main_content = get_object_or_404(MainContent, id=id)

    # Get all the photos associated with this MainContent
    photos = Photo.objects.filter(main_content=main_content)

    # Pass the main content and photos to the template
    context = {
        'main_content': main_content,
        'photos': photos
    }
    return render(request, "gallery_indi.html", context)

def services(request):
    return render(request, "services.html")

def index_services(request):
    return render(request, "index_services.html")

