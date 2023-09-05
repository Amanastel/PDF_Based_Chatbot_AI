"""
URL configuration for llmModelAi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views, pdfChat
from llmApp.views import *
from llmApp.pdfChat import *

urlpatterns = [
    path('',views.home,name='home'),
    path('pdf-chat/', pdf_chat, name='pdf_chat'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('convert-pdf/<int:pdf_id>/', views.convert_pdf_to_text, name='convert_pdf_to_text'),
    path('upload_pdf/', pdfChat.upload_pdf, name='upload_pdf'),
    path('ask_question/', pdfChat.ask_question, name='ask_question'),
    path('view_pdf/<int:pdf_id>/', pdfChat.view_pdf, name='view_pdf'),
    path('view_chat_history/', pdfChat.view_chat_history, name='view_chat_history'),
    
]
