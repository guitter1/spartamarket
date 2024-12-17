from django.db import models
from PIL import Image
from django.conf import settings

class Product(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    image=models.ImageField(upload_to="images/", blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,  related_name="products")
    like_users=models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_products")
    views = models.PositiveIntegerField(default=0) 
    hashtags=models.ManyToManyField('Hashtag', related_name="posts")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            image_path = self.image.path
            with Image.open(image_path) as img:
                max_width, max_height = 250, 250
                img.thumbnail((max_width, max_height))
                img.save(image_path, quality=85, optimize=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments")
    content = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments",)
    
    def __str__(self):
        return f"{self.author.username}: {self.content[:20]}"
    
class Hashtag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name    