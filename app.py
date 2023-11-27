import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
# from langchain.embeddings.openai import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.embeddings.huggingface import HuggingFaceInstructEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import OpenAI, HuggingFacePipeline
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import FAISS
from htmlTemplates import css, bot_template, user_template
from langchain.llms import HuggingFaceHub


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(raw_text):
    text_splitter = CharacterTextSplitter(separator="\n",chunk_size=1000, chunk_overlap=200,length_function=len)
    chunks = text_splitter.split_text(raw_text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = HuggingFaceInstructEmbeddings(model_name = "hkunlp/instructor-xl")
    # embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    return vector_store

def get_conversational_chain(vector_store):
    
    # llm=ChatOpenAI()
    llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversational_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever(),
        memory=memory,
    )
    return  conversational_chain

def handle_userinput(user_question):
    response = st.session_state.conversation_chain({'question': user_question})
    st.write(response)
    # st.session_state.chat_history = response['chat_history']
    
    # for i,message in enumerate(st.session_state.chat_history):
    
    #     if i%2==0:
    #         st.write(user_template.replace("{{MSG}}", message['content']), unsafe_allow_html=True)
    #     else:
    #         st.write(bot_template.replace("{{MSG}}", message['content']), unsafe_allow_html=True)
        

def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with multiple PDFs", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)
    st.title("Chat with multiple PDFs :books:")
    user_question = st.text_input("Ask a question about your docuemnts:")
    if user_question:
        handle_userinput(user_question)

    if "conversation_chain" not in st.session_state:
        st.session_state.conversation_chain = None

    # if "chat_history" not in st.session_state:
    #     st.session_state.chat_history = None
    
    st.write(user_template.replace("{{MSG}}", "hello robot"), unsafe_allow_html=True)
    st.write(bot_template.replace("{{MSG}}", "hello human"), unsafe_allow_html=True)
    
    with st.sidebar:
        st.subheader("Your docuemnts")
        pdf_docs = st.file_uploader("Upload your PDFS here and click on process", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("processsing"):   
                # get the pdf text
                raw_text = get_pdf_text(pdf_docs)
                # st.write(raw_text)
                #get the test chunks
                text_chunks = get_text_chunks(raw_text)
                # st.write(text_chunks)
                # get the vector store
                vector_store = get_vector_store(text_chunks)
                
                # converstation chain
                st.session_state.conversation_chain = get_conversational_chain(vector_store)
                
                
                

if __name__=='__main__':
    main()