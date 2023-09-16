# forms.py
from django import forms
from .models import PDFDocument, ChatMessage
from django.contrib.auth.forms import UserCreationForm
from .models import CustomProfile


class RegistrationForm(forms.ModelForm):
    """
    Form for user registration.

    Allows users to input their phone number and address when registering.

    :param forms.ModelForm: Model form for user registration.
    """
    class Meta:
        model = CustomProfile
        fields = ('phone', 'address')

class PDFDocumentForm(forms.ModelForm):
    """
    Form for PDF document information.

    Allows users to input the title and embedding when adding a PDF document.

    :param forms.ModelForm: Model form for PDF document information.
    """
    class Meta:
        model = PDFDocument
        fields = ['title', 'embedding']
        
       
class PDFDocumentForm2(forms.ModelForm):
    """
    Form for updating PDF document information.

    Allows users to edit the title, document content, and embedding of a PDF document.

    :param forms.ModelForm: Model form for updating PDF document information.
    """
    class Meta:
        model = PDFDocument
        fields = ['title', 'documentContent', 'embedding']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'documentContent': forms.Textarea(attrs={'class': 'form-control'}),
            'embedding': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Title',
            'documentContent': 'Document Content',
            'embedding': 'Embedding',
        } 

class PDFUpdateForm(forms.ModelForm):
    """
    Form for updating PDF document information.

    Allows users to edit the title, document content, and embedding of a PDF document.

    :param forms.ModelForm: Model form for updating PDF document information.
    """
    class Meta:
        model = PDFDocument
        fields = ['title', 'documentContent', 'embedding']
        
class PDFUploadForm(forms.Form):
    """
    Form for uploading a PDF document.

    Allows users to upload a PDF document.

    :param forms.Form: Form for uploading a PDF document.
    """
    pdf_document = forms.FileField(label='Upload a PDF', required=True)
    

class UserQuestionForm(forms.Form):
    """
    Form for user questions.

    Allows users to input their questions.

    :param forms.Form: Form for user questions.
    """
    user_question = forms.CharField(max_length=255, label='Your Question')

# class ChatMessageForm(forms.ModelForm):
#     class Meta:
#         model = ChatMessage
#         fields = ['message']




        
        
