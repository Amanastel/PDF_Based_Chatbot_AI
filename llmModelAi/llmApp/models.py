from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.models import AbstractUser

from django.contrib.auth.models import  Group, Permission

from django.utils.translation import gettext_lazy as _

class CustomProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    
    def __str__(self):
        return self.user.username
    

class PDFDocument(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    # document = models.FileField(upload_to='pdf_documents/')
    embedding = models.TextField()
    def __str__(self):
        return f"{self.user.username}'s PDF: {self.document.name}"

class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} at {self.timestamp}: {self.message}"
