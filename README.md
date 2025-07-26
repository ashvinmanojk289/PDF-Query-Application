# 💬 Chat With Your PDF using Google Gemini

An intelligent application to query and chat with your PDF documents using natural language.

## 🚀 Project Overview

The PDF Query Application is a powerful tool designed to streamline interactions with PDF documents. It transforms static PDFs into dynamic, conversational sources of information, allowing users to ask questions in natural language and receive detailed answers based on the document's content. This project leverages Google's state-of-the-art Gemini Pro model, the LangChain framework for building LLM applications, and FAISS for efficient similarity searches, all wrapped in a user-friendly interface built with Streamlit.

### 🎯 Key Features
- 📂 Multiple Document Support: Upload and process one or more PDF files at a time.
- 🗣️ Natural Language Interaction: Ask complex questions just as you would to a person.
- 🧠 Powered by Gemini Pro: Utilizes Google's advanced language model for high-quality, context-aware responses.
- ⚡ Fast & Efficient Search: Employs a FAISS vector store for rapid and relevant information retrieval from the documents.
- 💻 Simple Web Interface: A clean, intuitive, and easy-to-use application built with Streamlit.
- 🔗 Smart Text Chunking: Automatically breaks down large documents into manageable pieces for the language model to process effectively.
  
## 🧩 System Architecture

The application follows a logical pipeline to process and query your documents:
```
Upload PDFs → Extract Text (PyPDF2) → Split into Chunks → Generate Embeddings (Google) → Create FAISS Vector Store → User Asks Question → Similarity Search in FAISS → Feed Context & Question to Gemini Pro → Generate & Display Answer
```

## 🏗️ Tech Stack

| Task | Model |
|------|-------|
| Language | Python |
| Web Framework | Streamlit |
| LLM Framework | LangChain |
| LLM Provider | Google Gemini Pro|
| Text Extraction | PyPDF2 |
| Vector Database | FAISS (faiss-cpu) |
| Environment Mgmt | Python-dotenv |


## ⚙️ Setup & Installation

1. **Clone the repository**
```bash
git clone https://github.com/your-username/pdf-query-gemini.git
cd pdf-query-gemini
```

2. **Create and activate a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Linux/macOS
venv\Scripts\activate     # On Windows
```

3. **Install dependencies**
```bash
pip install -r Requirements.txt
```

4. **Set up your Google API Key**
   Create a .env file in the root directory.
   Add your API key to the file:
```bash
GOOGLE_API_KEY="YOUR_API_KEY_HERE"
```

5. **Run the Application**
```bash
streamlit run Python_Script.py
```

## 🧪 Evaluation

As detailed in the project paper, the system's effectiveness was evaluated through several methods:
- Performance Testing: To ensure the application can handle multiple concurrent user queries efficiently.
- User Acceptance Testing: Conducted with stakeholders to confirm the application meets end-user requirements and expectations.
- Model Precision: The underlying embedding models are evaluated using metrics like Inverse Mean Average Precision to ensure a low error rate in information retrieval (see Figure 2 in the project paper).

## 🖼️ Application Screenshots
Here's a look at the application in action, based on the figures from the project paper.

1. Main Interface
2. Uploading a PDF File
3. Processing the Document
4. Getting a Response

## 🤝 Contributing

We welcome contributions!  
If you have suggestions or improvements, feel free to open an issue or submit a pull request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a pull request

## 📝 Future Work

- Enhance the UI to show source chunks alongside the answer.
- Add support for other document formats like .docx, .txt, and URLs.
- Implement conversation history for follow-up questions.
- Containerize the application with Docker for easy deployment.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙌 Acknowledgements

- The Team members of this project: Anshul Raj S V, Ashvin Manoj, Arjun M, Cliff Andrew Oliver.
- Google for the Gemini Pro model.
- The LangChain and Streamlit communities.
- Facebook AI for the FAISS library.
