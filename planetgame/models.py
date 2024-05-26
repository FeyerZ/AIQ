from django.db import models

class Planet(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    image_url = models.URLField()

    def __str__(self):
        return self.name
# Create your models here.
