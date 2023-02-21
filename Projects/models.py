from django.db import models


class Project(models.Model):
    project_name = models.CharField(max_length=100, unique=True, null=False)
    project_description = models.CharField(max_length=200)
    project_file = models.FileField(upload_to='projects/')
    authors = models.CharField(max_length=200)

    def __str__(self):
        return self.project_name