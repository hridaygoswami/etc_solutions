from django.urls import path 

from . import views

urlpatterns = [
    path("", views.index, name='Index'),
    path("about/", views.about, name='About'),
    path("contact/", views.contact, name='Contact'),
    path("gallery/", views.gallery, name='Gallery'),
    path("gallery/<int:id>", views.gallery_more, name='Gallery_more'),
    path("services/", views.services, name='Services'),
    path("index_services/", views.index_services, name='Index Services')
]