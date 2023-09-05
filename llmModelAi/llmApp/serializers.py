from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth import get_user_model
from rest_framework import serializers
from.models import ChatMessage, PDFDocument

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password']
        
        
class PDFDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PDFDocument
        fields = ['id','user' ,'title', 'document', 'embedding']