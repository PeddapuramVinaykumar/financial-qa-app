import streamlit as st
import pdfplumber
import pandas as pd
import ollama   # Python client for Ollama

# ----------------------
# Helper functions
# ----------------------
def parse_pdf(file):
    """Extract text from PDF file, page by page"""
    chunks = []
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            if text.strip():
                chunks.append(text)
    return chunks

def parse_excel(file):
    """Extract text from Excel file by converting to CSV string"""
    df = pd.read_excel(file)
    return [df.to_csv(index=False)]

# Simple in-memory "index"
INDEX = []

def add_to_index(chunk, metadata=None):
    INDEX.append({"text": chunk, "metadata": metadata})

def retrieve(query, top_k=3):
    # Dummy retrieval: just return first k chunks
    return INDEX[:top_k]

# ----------------------
# Streamlit UI
# ----------------------
st.set_page_config(page_title="Financial Q&A", layout="wide")
st.title("📊 Financial Document Q&A")

# File upload
uploaded_file = st.file_uploader("Upload PDF or Excel file", type=["pdf", "xls", "xlsx"])
if uploaded_file:
    st.info(f"Processing {uploaded_file.name}...")

    if uploaded_file.name.endswith(".pdf"):
        chunks = parse_pdf(uploaded_file)
    else:
        chunks = parse_excel(uploaded_file)

    for chunk in chunks:
        add_to_index(chunk, {"text": chunk})

    st.success("✅ Document processed successfully!")

# Question input
question = st.text_input("Ask a question about your financial document:")
if question:
    st.info("Generating answer...")
    contexts = retrieve(question)
    context_text = "\n".join([c["text"] for c in contexts])

    # Ask Ollama model
    prompt = f"Answer the question using only the following context:\n{context_text}\nQuestion: {question}"
    try:
        response = ollama.chat(
            model="mistral",   # or "llama2" if you pulled that
            messages=[{"role": "user", "content": prompt}]
        )
        answer = response["message"]["content"]
    except Exception as e:
        answer = f"⚠️ Could not connect to Ollama. Make sure it's running.\n\nDetails: {str(e)}"

    st.write("**Answer:**")
    st.write(answer)
