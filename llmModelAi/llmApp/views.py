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
from .models import ChatMessage, PDFDocument
from langchain.chat_models import ChatOpenAI
from django.contrib.auth.decorators import login_required
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from django.http import HttpResponse, JsonResponse
import fitz  # PyMuPDF
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from dotenv import load_dotenv


os.getenv('OPENAI_API_KEY')


# Create your views here.
@login_required(login_url="/login/")
def home(request):
    pdf_documents = PDFDocument.objects.filter(user=request.user)
    return render(request, 'home.html', {'pdf_documents': pdf_documents})





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



























# my old code

# import os
# # pdf_chatbot_app/views.py
# from django.shortcuts import render
# from PyPDF2 import PdfReader
# from langchain.text_splitter import CharacterTextSplitter
# from langchain.embeddings.openai import OpenAIEmbeddings
# from langchain.vectorstores import FAISS
# from langchain.chains.question_answering import load_qa_chain
# from langchain.llms import OpenAI
# from langchain.callbacks import get_openai_callback
# from .forms import RegistrationForm
# from django.contrib.auth import login, authenticate, logout
# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.contrib.auth.models import User
# from .models import ChatMessage
# from langchain.chat_models import ChatOpenAI
# from django.contrib.auth.decorators import login_required
# from langchain.memory import ConversationBufferMemory
# from langchain.chains import ConversationalRetrievalChain
# from django.http import HttpResponse, JsonResponse
# import fitz  # PyMuPDF

# os.environ["OPENAI_API_KEY"] = "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"

# # Create your views here.

# def home(request):
#     return render(request, 'home.html')

# pdfname=None
# pdfsize=None
# scripttext=None

# def get_vectorstore(text_chunks):
#     embeddings = OpenAIEmbeddings()
#     # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
#     vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
#     return vectorstore

# def get_conversation_chain(vectorstore):
#     llm = ChatOpenAI()
#     # llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})

#     memory = ConversationBufferMemory(
#         memory_key='chat_history', return_messages=True)
#     conversation_chain = ConversationalRetrievalChain.from_llm(
#         llm=llm,
#         retriever=vectorstore.as_retriever(),
#         memory=memory
#     )
#     return conversation_chain


# def get_pdf_text(pdf, user_question):
#     if pdf:
#         pdf_reader = PdfReader(pdf)
#         text = ''.join(page.extract_text() for page in pdf_reader.pages)
#     return text

# def get_text_chunks(text):
#     text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len)
#     chunks = text_splitter.split_text(text)
#     # print(chunks)
#     return chunks



# def process_uploaded_pdfs(uploaded_pdfs, user_question):
#     global vector_store, conversation_chain
#     global pdfname, pdfsize, scripttext
#     raw_text = get_pdf_text(uploaded_pdfs,user_question)
#     print("Extracted PDF text:", raw_text)
#     text_chunks = get_text_chunks(raw_text)
#     vector_store = get_vectorstore(text_chunks)
#     conversation_chain = get_conversation_chain(vector_store)
#     return({"pdfname":pdfname,"pdfsize": pdfsize,"scripttext": scripttext})


# @login_required
# def pdf_chat(request):
#     chat_response = ''
#     chat_history = ChatMessage.objects.filter(user=request.user).order_by('timestamp')  # Retrieve chat history for the logged-in user

#     if request.method == 'POST':
#         pdf = request.FILES.get('pdf')
#         print("start")     
#         user_question = request.POST.get('question')
#         pdfFun = process_uploaded_pdfs(pdf, user_question)
#         print(200)
#         # print(pdfFun)
#         print(2040)

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
            
#             # create vector store
#             vectorstore = get_vectorstore(chunks)
            
#              # create conversation chain
#             conversationChain = get_conversation_chain(vectorstore)
            
#             # Save the chat message to the database
#             chat_message = ChatMessage(user=request.user, message=user_question, answer=chat_response)
#             chat_message.save()

#     context = {'chat_response': chat_response, 'chat_history': chat_history}
#     return render(request, 'pdf_chatbot.html', context)



# def register(request):
#     if request.method == 'POST':
#         data = request.POST
#         first_name = data.get("first_name")
#         last_name = data.get("last_name")
#         username = data.get("username")
#         password = data.get("password")
#         email = data.get("email")
        
#         user = User.objects.filter(username = username)
        
#         if user.exists():
#             messages.info(request, "username already Taken")
#             return redirect("/register/")
        
#         user_email = User.objects.filter(email = email)
        
#         if user_email.exists():
#             messages.info(request, "email already Taken")
#             return redirect("/register/")
        
#         user = User.objects.create_user(
#             username=username,
#             email=email,
#             first_name=first_name,
#             last_name=last_name,
#         )
        
#         user.set_password(password)
#         user.save()
        
#         messages.info(request, "Account created successfully")
        
#         return redirect("/register/")
#     return render(request, 'register.html')




# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('home')  # Redirect to the home page or any other desired page
#         else:
#             messages.error(request, 'Invalid username or password. Please try again.')
#     return render(request, 'login.html')

# def user_logout(request):
#     logout(request)
#     return redirect('login')









# new code 

# pdfname=None
# pdfsize=None
# scripttext=None

# def get_vectorstore(text_chunks):
#     embeddings = OpenAIEmbeddings()
#     vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
#     return vectorstore

# def get_conversation_chain(vectorstore):
#     llm = ChatOpenAI()
#     memory = ConversationBufferMemory(
#         memory_key='chat_history', return_messages=True)
#     conversation_chain = ConversationalRetrievalChain.from_llm(
#         llm=llm,
#         retriever=vectorstore.as_retriever(),
#         memory=memory
#     )
#     return conversation_chain


# def get_pdf_text(pdf):
#     if pdf:
#         pdf_reader = PdfReader(pdf)
#         text = ''.join(page.extract_text() for page in pdf_reader.pages)
#     return text

# def get_text_chunks(text):
#     text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len)
#     chunks = text_splitter.split_text(text)
#     # print(chunks)
#     return chunks



# def process_uploaded_pdfs(uploaded_pdfs, user_question):
#     global vector_store, conversation_chain
#     global pdfname, pdfsize, scripttext
#     raw_text = get_pdf_text(uploaded_pdfs,user_question)
#     # print("Extracted PDF text:", raw_text)
#     text_chunks = get_text_chunks(raw_text)
#     vector_store = get_vectorstore(text_chunks)
#     conversation_chain = get_conversation_chain(vector_store)
#     return({"pdfname":pdfname,"pdfsize": pdfsize,"scripttext": scripttext})


# def convert_pdf_to_text(pdf_document, request):
#     chat_message = ChatMessage(user=request.user, message=user_question, answer=chat_response)
#     chat_message.save()
#     try:
#         # pdf_document = get_object_or_404(PDFDocument)
#         pdf_text = get_pdf_text(pdf_document)
        
#         if pdf_text:
#             pdfs = PDFDocument(user=request.user, title=pdf_document.name, documentContent=pdf_text, embedding=pdf_text)
#             # Save the extracted text to the 'documentContent' field
#             pdf_document = pdf_text
#             pdf_document.save()
            
#             return JsonResponse({'success': True, 'message': 'PDF text saved successfully.'})
#         else:
#             return JsonResponse({'success': False, 'message': 'Error extracting text from the PDF.'})
#     except PDFDocument.DoesNotExist:
#         return JsonResponse({'success': False, 'message': 'PDF document not found.'})
    
# def extract_pdf_text(pdf_file_path):
#     try:
#         pdf_reader = PdfReader(pdf_file_path)
#         text = ''.join(page.extract_text() for page in pdf_reader.pages)
#         return text
#     except Exception as e:
#         print(f"Error extracting text from PDF: {str(e)}")
#         return None


# @login_required
# def pdf_chat(request):
#     chat_response = ''
#     chat_history = ChatMessage.objects.filter(user=request.user).order_by('timestamp')  # Retrieve chat history for the logged-in user

#     if request.method == 'POST':
#         pdf = request.FILES.get('pdf')
#         print("start")     
#         user_question = request.POST.get('question')
#         # pdfFun = process_uploaded_pdfs(pdf, user_question)
#         print(200)
#         # print(pdfFun)
#         print(2040)
#         # if pdf:
#         #     convert_pdf_to_text(pdf,request)
            
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
#             print("prinng chunks")
#             print(chunks)

#             # Create embeddings and knowledge base
#             embeddings = OpenAIEmbeddings()
#             knowledge_base = FAISS.from_texts(chunks, embeddings)
#             # print("prinng embeddings")
#             # print(embeddings)
            
#             # pdfs = PDFDocument(user=request.user, title=pdf.name, documentContent=chunks, embedding=knowledge_base)
#             # pdfs.save()
            
#             # Perform similarity search
#             docs = knowledge_base.similarity_search(user_question)

#             # Load LangChain model and run question answering
#             llm = OpenAI()
#             chain = load_qa_chain(llm, chain_type="stuff")
#             with get_openai_callback() as cb:
#                 response = chain.run(input_documents=docs, question=user_question)

#             chat_response = response
            
#             # create vector store
#             vectorstore = get_vectorstore(chunks)
            
#              # create conversation chain
#             conversationChain = get_conversation_chain(vectorstore)
            
#             # Save the chat message to the database
#             chat_message = ChatMessage(user=request.user, message=user_question, answer=chat_response)
#             chat_message.save()

#     context = {'chat_response': chat_response, 'chat_history': chat_history}
#     return render(request, 'pdf_chatbot.html', context)

