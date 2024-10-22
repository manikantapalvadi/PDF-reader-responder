import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_groq import ChatGroq
from app_styling import css, bot_template, user_template


def get_pdf_text(docs):
    text = ""
    for pdf in docs:
        try:
            pdf_reader = PdfReader(pdf)
            for page in pdf_reader.pages:
                extracted_text = page.extract_text()
                if extracted_text:
                    text += extracted_text
                else:
                    st.warning(f"No text found on page {pdf_reader.pages.index(page)} in {pdf.name}")
        except Exception as e:
            st.error(f"Error reading {pdf.name}: {e}")
    return text



def get_pdf_text_chunks(raw_text):
    text_splitter = CharacterTextSplitter(
        separator = '\n',
        chunk_size = 1000,
        chunk_overlap = 200,
        length_function = len
    )

    chunks = text_splitter.split_text(raw_text)
    return chunks

def get_vectostore(text_chunks):
    embeddings  = HuggingFaceInstructEmbeddings(model_name = 'hkunlp/instructor-large')
    vectorstore = FAISS.from_texts(texts = text_chunks, embedding = embeddings)
    return vectorstore

def get_conversation_chain(vectorstore):
    llm = ChatGroq(model="llama3-70b-8192")
    memory = ConversationBufferMemory(memory_key= 'chat_history',return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(llm = llm, retriever = vectorstore.as_retriever(), memory = memory)
    return conversation_chain

def handle_user_input(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i,message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}",message.content),unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}",message.content),unsafe_allow_html=True)

def main():
    load_dotenv()
    st.set_page_config(page_title="PDFIQ", page_icon=":books:")
    st.write(css,unsafe_allow_html=True)


    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with your PDFs :books:")
    user_question = st.text_input("Ask question about the content from PDFs you uploaded:")
    if user_question:
        handle_user_input(user_question)

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader("Upload your PDFs here...",accept_multiple_files=True)
        if st.button("Upload"):
            with st.spinner("Processing "):
                # Get text
                raw_text = get_pdf_text(pdf_docs)
                
                # create chunks
                text_chunks = get_pdf_text_chunks(raw_text)

                # create vectorstore
                vectorstore = get_vectostore(text_chunks)

                # conversations
                st.session_state.conversation = get_conversation_chain(vectorstore)
                st.write("I read it Buddy")




if __name__ == '__main__':
    main()