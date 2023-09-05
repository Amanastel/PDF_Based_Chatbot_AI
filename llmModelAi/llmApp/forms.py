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
        
        
        
class PDFUploadForm(forms.Form):
    pdf_document = forms.FileField(label='Upload a PDF', required=True)
    

class UserQuestionForm(forms.Form):
    user_question = forms.CharField(max_length=255, label='Your Question')

# class ChatMessageForm(forms.ModelForm):
#     class Meta:
#         model = ChatMessage
#         fields = ['message']
