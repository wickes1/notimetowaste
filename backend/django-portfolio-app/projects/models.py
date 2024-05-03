from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    technology = models.CharField(max_length=20)
    image = models.FileField(upload_to="projects_images/", blank=True)
