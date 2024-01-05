from django.db import models
from django.contrib.auth.models import User 
from django.utils.text import slugify


class Category(models.Model):
    title = models.CharField(("Başlık"), max_length=50)
    slug = models.SlugField(("Slug"))
    
    def __str__(self):
        return self.title
        



class Contents(models.Model):
    # title = models.CharField(("Başlık"), null = True, max_length=50)
    image = models.ImageField(("Resim"), upload_to="contents")
    category= models.ForeignKey(Category, verbose_name=("Kategori"), null=True, on_delete=models.CASCADE)
    





