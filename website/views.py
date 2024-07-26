from django.shortcuts import render
from django.http import HttpResponse
from .models import MainContent, Category
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

def gallery_more(request, id):
    # return HttpResponse(f"This is gallery ph id {id}")
    return render("gallery_main.html", {
        "id": id
    })

def services(request):
    return render(request, "services.html")

def index_services(request):
    return render(request, "index_services.html")

