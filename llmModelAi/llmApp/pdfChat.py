
from django.shortcuts import render
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
from .forms import RegistrationForm, PDFUploadForm
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
from django.views import View
import os


vector_store = None
conversation_chain = None 

pdfname=None
pdfsize=None
scripttext=None

def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    knowledge_base = FAISS.from_texts(text_chunks, embeddings)
    return knowledge_base

def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    # llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


def get_pdf_text(pdf):
    if pdf:
        pdf_reader = PdfReader(pdf)
        text = ''.join(page.extract_text() for page in pdf_reader.pages)
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len)
    chunks = text_splitter.split_text(text)
    # print(chunks)
    return chunks

def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

    
    
def upload_pdf(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_document = request.FILES['pdf_document']
            # title = request.POST.get('title', )
            # Save the PDF document to the database and process it here
            pdf = PDFDocument(user=request.user, title=pdf_document.name)
            pdf.save()
            pdf.documentContent = process_uploaded_pdf(pdf_document)
            pdf.save()
            return JsonResponse({'message': 'PDF uploaded successfully.'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid form data.'}, status=400)
    else:
        form = PDFUploadForm()
    return render(request, 'upload_pdf.html', {'form': form})

def process_uploaded_pdf(pdf_file):
    raw_text = get_pdf_text(pdf_file)
    # print("Extracted PDF text:", raw_text)
    text_chunks = get_text_chunks(raw_text)
    # print(text_chunks)
    return text_chunks



def ask_question(request):
    chat_response= ''
    user_pdfs = PDFDocument.objects.filter(user=request.user)
    if request.method == 'POST':
        user_question = request.POST.get('user_question')
        selected_pdf_id = request.POST.get('selected_pdf')
        selected_pdf = get_object_or_404(PDFDocument, id=selected_pdf_id)
        
        # embeddings = OpenAIEmbeddings()
        # document = FAISS.from_texts(selected_pdf.documentContent,embeddings)
        # similarSearch = document.similarity_search(user_question)
        
        # llm = OpenAI()
        # chain = load_qa_chain(llm,chain_type="stuff")
        # answer = chain.run(input_documents=similarSearch,question=user_question)
        
        # print(answer)
        
        knowledge_base = get_vectorstore(selected_pdf.documentContent)
        
        docs = knowledge_base.similarity_search(user_question)
        
        # llm = ChatOpenAI(openai_api_key=os.environ.get('OPENAI_API_KEY'))
        # memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
        # conversation_chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=knowledge_base.as_retriever(), memory=memory)
        
        # if not conversation_chain:
        #     return {"status": "error", "message": "Please upload and process PDFs first."}
        # response = conversation_chain({'question': user_question})
        # print(response)
        
        llm = OpenAI()
        chain = load_qa_chain(llm, chain_type="stuff")
        with get_openai_callback() as cb:
                response = chain.run(input_documents=docs, question=user_question)
        #         # print(response)
        
        chat_response = response
        print(chat_response)
    return render(request, 'ask_question.html', {'user_pdfs': user_pdfs})


def process_user_question(pdf, user_question):
    embeddings = OpenAIEmbeddings()
    knowledge_base = FAISS.from_texts(pdf, embeddings)
    
    docs = knowledge_base.similarity_search(user_question)
    
    llm = OpenAI()
    chain = load_qa_chain(llm, chain_type="stuff")
    with get_openai_callback() as cb:
        response = chain.run(input_documents=docs, question=user_question)
        
        return response

    

def view_pdf(request, pdf_id):
    pdf = PDFDocument.objects.get(id=pdf_id)
    return render(request, 'view_pdf.html', {'pdf': pdf})

def view_chat_history(request):
    chat_messages = ChatMessage.objects.filter(user=request.user)
    return render(request, 'view_chat_history.html', {'chat_messages': chat_messages})