from django.contrib import admin
from .models import Category, MainContent, Photo

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1
    max_num = 10

@admin.register(MainContent)
class MainContentAdmin(admin.ModelAdmin):
    list_display = ('category', 'date', 'description')
    search_fields = ('description',)
    inlines = [PhotoInline]

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('main_content', 'image')
