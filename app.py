import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate

# --- CONFIGURATION ---
st.set_page_config(page_title="Chat with PDFs", page_icon="💬")

# Load API key from Streamlit secrets
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except (KeyError, AttributeError):
    st.error("⚠️ Google API Key not found. Please add it to your Streamlit secrets.", icon="🚨")
    st.stop()


# --- CORE FUNCTIONS ---
def get_pdf_text(pdf_docs):
    """Extracts text from a list of uploaded PDF files."""
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text

def get_text_chunks(text):
    """Splits the text into manageable chunks."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    """Creates a FAISS vector store from text chunks."""
    if not text_chunks:
        st.warning("Could not extract any text from the PDF(s). Please check the documents.", icon="⚠️")
        return None
    try:
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
        return vector_store
    except Exception as e:
        st.error(f"Error creating vector store: {e}", icon="🚨")
        return None

def get_conversational_chain():
    """Creates a conversational QA chain with a custom prompt."""
    prompt_template = """
    Answer the question as detailed as possible from the provided context. 
    Make sure to provide all the details. If the answer is not in the provided context, 
    just say, "The answer is not available in the context." Do not provide a wrong answer.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

# --- INITIALIZE SESSION STATE ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

# --- STREAMLIT APP LAYOUT ---
st.header("Chat with Your PDFs using Gemini Pro 💬")

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if user_question := st.chat_input("Ask a question about your documents..."):
    st.session_state.chat_history.append({"role": "user", "content": user_question})
    with st.chat_message("user"):
        st.markdown(user_question)

    if st.session_state.vector_store:
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    docs = st.session_state.vector_store.similarity_search(user_question)
                    
                    if not docs:
                         response_text = "I couldn't find any relevant information in the documents to answer your question."
                    else:
                        chain = get_conversational_chain()
                        response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
                        response_text = response["output_text"]

                    st.markdown(response_text)
                    st.session_state.chat_history.append({"role": "assistant", "content": response_text})
                except Exception as e:
                    error_message = f"An error occurred: {e}"
                    st.error(error_message)
                    st.session_state.chat_history.append({"role": "assistant", "content": error_message})
    else:
        with st.chat_message("assistant"):
            response_text = "Please upload and process your PDF documents first using the sidebar."
            st.warning(response_text, icon="⚠️")
            st.session_state.chat_history.append({"role": "assistant", "content": response_text})


# --- SIDEBAR FOR FILE UPLOAD ---
with st.sidebar:
    st.title("Menu")
    st.write("Upload your PDF files and click 'Process' to start chatting.")
    pdf_docs = st.file_uploader("Upload PDF Files", accept_multiple_files=True, type="pdf")

    if st.button("Process Documents"):
        if pdf_docs:
            with st.spinner("Processing documents..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                vector_store = get_vector_store(text_chunks)

                if vector_store:
                    st.session_state.vector_store = vector_store
                    st.success("Processing complete! You can now ask questions.", icon="✅")
                    st.session_state.chat_history = [] 
                else:
                    st.error("Failed to process documents.", icon="🚨")
        else:
            st.warning("Please upload at least one PDF file.", icon="⚠️")
