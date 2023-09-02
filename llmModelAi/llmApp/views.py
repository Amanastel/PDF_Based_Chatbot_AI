import os
# pdf_chatbot_app/views.py
from django.shortcuts import render
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
from .forms import RegistrationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import ChatMessage
from django.contrib.auth.decorators import login_required




# Create your views here.

def home(request):
    return render(request, 'home.html')



# def pdf_chat(request):
#     chat_response = ''

#     if request.method == 'POST':
#         pdf = request.FILES.get('pdf')
#         user_question = request.POST.get('question')

#         if pdf and user_question:
#             pdf_reader = PdfReader(pdf)
#             text = ''.join(page.extract_text() for page in pdf_reader.pages)

#             # Split text into chunks
#             text_splitter = CharacterTextSplitter(
#                 separator="\n",
#                 chunk_size=1000,
#                 chunk_overlap=200,
#                 length_function=len
#             )
#             chunks = text_splitter.split_text(text)
#             print(chunks)

#             # Create embeddings and knowledge base
#             embeddings = OpenAIEmbeddings()
#             knowledge_base = FAISS.from_texts(chunks, embeddings)
#             print("inside the knowledge_base")
            

#             # Perform similarity search
#             docs = knowledge_base.similarity_search(user_question)

#             # Load LangChain model and run question answering
#             llm = OpenAI()
#             chain = load_qa_chain(llm, chain_type="stuff")
#             with get_openai_callback() as cb:
#                 response = chain.run(input_documents=docs, question=user_question)

#             chat_response = response

#     context = {'chat_response': chat_response}
#     return render(request, 'pdf_chatbot.html', context)



# @login_required
# def pdf_chat(request):
#     chat_response = ''
#     chat_history = ChatMessage.objects.all()  # Retrieve all chat history

#     if request.method == 'POST':
#         pdf = request.FILES.get('pdf')
#         user_question = request.POST.get('question')

#         if pdf and user_question:
#             pdf_reader = PdfReader(pdf)
#             text = ''.join(page.extract_text() for page in pdf_reader.pages)

#             # Split text into chunks
#             text_splitter = CharacterTextSplitter(
#                 separator="\n",
#                 chunk_size=1000,
#                 chunk_overlap=200,
#                 length_function=len
#             )
#             chunks = text_splitter.split_text(text)

#             # Create embeddings and knowledge base
#             embeddings = OpenAIEmbeddings()
#             knowledge_base = FAISS.from_texts(chunks, embeddings)

#             # Perform similarity search
#             docs = knowledge_base.similarity_search(user_question)

#             # Load LangChain model and run question answering
#             llm = OpenAI()
#             chain = load_qa_chain(llm, chain_type="stuff")
#             with get_openai_callback() as cb:
#                 response = chain.run(input_documents=docs, question=user_question)

#             chat_response = response

#             # Save the chat message to the database
#             chat_message = ChatMessage(user=request.user, message=user_question, answer=chat_response)
#             chat_message.save()

#     context = {'chat_response': chat_response, 'chat_history': chat_history}
#     return render(request, 'pdf_chatbot.html', context)

@login_required
def pdf_chat(request):
    chat_response = ''
    chat_history = ChatMessage.objects.filter(user=request.user).order_by('timestamp')  # Retrieve chat history for the logged-in user

    if request.method == 'POST':
        pdf = request.FILES.get('pdf')
        user_question = request.POST.get('question')

        if pdf and user_question:
            pdf_reader = PdfReader(pdf)
            text = ''.join(page.extract_text() for page in pdf_reader.pages)

            # Split text into chunks
            text_splitter = CharacterTextSplitter(
                separator="\n",
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len
            )
            chunks = text_splitter.split_text(text)

            # Create embeddings and knowledge base
            embeddings = OpenAIEmbeddings()
            knowledge_base = FAISS.from_texts(chunks, embeddings)

            # Perform similarity search
            docs = knowledge_base.similarity_search(user_question)

            # Load LangChain model and run question answering
            llm = OpenAI()
            chain = load_qa_chain(llm, chain_type="stuff")
            with get_openai_callback() as cb:
                response = chain.run(input_documents=docs, question=user_question)

            chat_response = response

            # Save the chat message to the database
            chat_message = ChatMessage(user=request.user, message=user_question, answer=chat_response)
            chat_message.save()

    context = {'chat_response': chat_response, 'chat_history': chat_history}
    return render(request, 'pdf_chatbot.html', context)



def register(request):
    if request.method == 'POST':
        data = request.POST
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        username = data.get("username")
        password = data.get("password")
        email = data.get("email")
        
        user = User.objects.filter(username = username)
        
        if user.exists():
            messages.info(request, "username already Taken")
            return redirect("/register/")
        
        user_email = User.objects.filter(email = email)
        
        if user_email.exists():
            messages.info(request, "email already Taken")
            return redirect("/register/")
        
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        
        user.set_password(password)
        user.save()
        
        messages.info(request, "Account created successfully")
        
        return redirect("/register/")
    return render(request, 'register.html')




def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to the home page or any other desired page
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')