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

os.environ["OPENAI_API_KEY"] = "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"

# Create your views here.

def home(request):
    return render(request, 'home.html')



def pdf_chat(request):
    chat_response = ''

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

    context = {'chat_response': chat_response}
    return render(request, 'pdf_chat.html', context)
