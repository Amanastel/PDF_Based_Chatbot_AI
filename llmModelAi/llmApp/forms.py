# forms.py
from django import forms
from .models import PDFDocument, ChatMessage
from django.contrib.auth.forms import UserCreationForm
from .models import CustomProfile


class CustomProfileForm(forms.ModelForm):
    class Meta:
        model = CustomProfile
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'address']

class PDFDocumentForm(forms.ModelForm):
    class Meta:
        model = PDFDocument
        fields = ['title', 'document', 'embedding']
        

class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['message']
