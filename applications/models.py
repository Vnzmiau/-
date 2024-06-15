from django.db import models
from django.contrib.auth.models import User

class Application(models.Model):
    applicant=models.OneToOneField(User,on_delete=models.SET_NULL,null=True)
    profession=models.CharField(max_length=100)
    education=models.TextField()
    work_experience=models.TextField()
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)
    file=models.FileField()
    

    def __str__(self):
        return self.name
    

# Create your models here.
