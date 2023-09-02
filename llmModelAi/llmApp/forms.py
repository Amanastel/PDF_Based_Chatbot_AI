# forms.py
from django import forms
from .models import PDFDocument, ChatMessage
from django.contrib.auth.forms import UserCreationForm
from .models import CustomProfile


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = CustomProfile
        fields = ('phone', 'address')

class PDFDocumentForm(forms.ModelForm):
    class Meta:
        model = PDFDocument
        fields = ['title', 'embedding']
        

# class ChatMessageForm(forms.ModelForm):
#     class Meta:
#         model = ChatMessage
#         fields = ['message']
