from django.db import models
from PIL import Image

class Product(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    image=models.ImageField(upload_to="images/", blank=True)

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
