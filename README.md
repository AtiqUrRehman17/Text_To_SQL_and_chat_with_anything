### 🧠 Text-to-SQL and Chat-with-Anything

This project is an AI-powered assistant that can do two main things:

Text to SQL – You can type your question in normal English, and it will automatically turn it into a proper PostgreSQL query and run it on your database.

Chat with Files – You can upload PDF, TXT, CSV, or DOCX files and ask questions about their content.

You can use it either from the command line (CLI) or with a Streamlit web interface.


### 🚀 Features

✅ Convert natural language into SQL queries (Text-to-SQL)
✅ Connect and run queries on your PostgreSQL database
✅ Upload and chat with multiple file types (PDF, TXT, CSV, DOCX)
✅ Works with Groq’s Llama 3.1 model for fast AI responses
✅ Includes both terminal and Streamlit web app versions
✅ Easy to set up using environment variables


### 🧩 Project Structure
text_to_sql_and_chat_with_anything/
│
├── db.py                # Handles database connection and query execution
├── llm_chain.py         # Converts natural text into SQL using Groq’s LLM
├── file_processor.py    # Reads and processes files (PDF, TXT, CSV, DOCX)
├── chat_with_files.py   # CLI interface to chat with uploaded files
├── main.py              # Main CLI entry point
├── streamlit_app.py     # Streamlit web app
├── .env.example         # Example environment variables
└── requirements.txt     # Python dependencies


### 🧠 Tech Stack

Python 3.9+

Streamlit – for the web interface

LangChain + Groq LLM (Llama 3.1) – for text-to-SQL and file Q&A

SQLAlchemy + psycopg2 – for database access

PyPDF2, python-docx, pandas – for reading uploaded files

### 🪶 Example

### Question:

Show me all employees who joined after January 2023.

Generated SQL:

SELECT * FROM employees WHERE join_date > '2023-01-01';

⚡ Notes

Make sure your database is running before using the Text-to-SQL feature.

You’ll need a valid Groq API key to use the AI models.

Large PDFs or image-based files may not extract text perfectly.