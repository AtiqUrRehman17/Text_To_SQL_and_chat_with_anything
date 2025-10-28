import streamlit as st
import os
import tempfile
from llm_chain import natural_to_sql
from db import execute_sql
from file_processor import FileProcessor

# Page configuration
st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS for simple styling
st.markdown("""
<style>
    .main-title {
        text-align: center;
        color: #1f77b4;
        font-size: 2.5rem;
        margin-bottom: 2rem;
    }
    .feature-button {
        width: 100%;
        height: 80px;
        font-size: 1.2rem;
        margin: 10px 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'file_processor' not in st.session_state:
    st.session_state.file_processor = FileProcessor()
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'current_mode' not in st.session_state:
    st.session_state.current_mode = None

def show_text_to_sql():
    """Show Text-to-SQL interface"""
    st.markdown("## 🔍 Text-to-SQL")
    st.write("Convert your natural language questions to SQL queries")
    
    question = st.text_area(
        "Enter your question:",
        placeholder="e.g., Show me all users who signed up last month...",
        height=100
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🚀 Convert to SQL", use_container_width=True):
            if question:
                with st.spinner("Converting to SQL..."):
                    sql_query = natural_to_sql(question)
                
                st.markdown("**Generated SQL:**")
                st.code(sql_query, language="sql")
                
                with st.spinner("Executing query..."):
                    columns, result = execute_sql(sql_query)
                
                if columns:
                    st.markdown("**Results:**")
                    st.dataframe(result)
                else:
                    st.info(result)
            else:
                st.warning("Please enter a question first")
    
    with col2:
        if st.button("⬅️ Back to Main Menu", use_container_width=True):
            st.session_state.current_mode = None
            st.rerun()

def show_file_chat():
    """Show File Chat interface"""
    st.markdown("## 📁 Chat with Files")
    st.write("Upload files and ask questions about their content")
    
    # File upload section
    st.markdown("### 📤 Upload Files")
    uploaded_file = st.file_uploader(
        "Choose a file (PDF, TXT, CSV, DOCX)",
        type=['pdf', 'txt', 'csv', 'docx'],
        key="file_uploader"
    )
    
    if uploaded_file is not None:
        # Check if file is already processed
        existing_files = [f['name'] for f in st.session_state.file_processor.get_uploaded_files()]
        if uploaded_file.name not in existing_files:
            with st.spinner(f"Processing {uploaded_file.name}..."):
                # Get file type from extension
                file_type = uploaded_file.name.split('.')[-1].lower()
                result = st.session_state.file_processor.process_uploaded_file(
                    uploaded_file.name, 
                    uploaded_file.getvalue(), 
                    file_type
                )
            
            if result.startswith("✅"):
                st.success(result)
            else:
                st.error(result)
        else:
            st.info(f"File {uploaded_file.name} is already processed")
    
    # Show uploaded files
    files = st.session_state.file_processor.get_uploaded_files()
    if files:
        st.markdown("### 📚 Your Files")
        for file_info in files:
            st.write(f"📄 **{file_info['name']}** ({file_info.get('size', 0)} characters)")
        
        # Clear files button
        if st.button("🗑️ Clear All Files", use_container_width=True):
            st.session_state.file_processor.clear_files()
            st.session_state.chat_history = []
            st.success("All files cleared!")
            st.rerun()
    
    # Chat section
    st.markdown("### 💬 Chat")
    
    if not files:
        st.info("📁 Upload files above to start chatting")
    else:
        # Display chat history
        for chat in st.session_state.chat_history:
            if chat['type'] == 'user':
                st.markdown(f"**You:** {chat['content']}")
            else:
                st.markdown(f"**Assistant:** {chat['content']}")
        
        # Chat input
        chat_input = st.text_input(
            "Ask a question about your files:",
            placeholder="What information is in the documents?",
            key="chat_input"
        )
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            if st.button("💬 Send", use_container_width=True, disabled=not chat_input):
                # Add user message to history
                st.session_state.chat_history.append({
                    'type': 'user',
                    'content': chat_input
                })
                
                # Get AI response
                with st.spinner("Thinking..."):
                    response = st.session_state.file_processor.chat_with_files(chat_input)
                
                # Add AI response to history
                st.session_state.chat_history.append({
                    'type': 'assistant',
                    'content': response
                })
                
                st.rerun()
        
        with col2:
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()
        
        with col3:
            if st.button("⬅️ Back to Main", use_container_width=True):
                st.session_state.current_mode = None
                st.rerun()

def main():
    # Main title
    st.markdown('<div class="main-title">🧠 AI Assistant</div>', unsafe_allow_html=True)
    
    # If no mode selected, show main menu
    if st.session_state.current_mode is None:
        st.markdown("### Choose what you want to do:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔍 Text-to-SQL\n\nConvert natural language to SQL queries", 
                        use_container_width=True, 
                        key="text_to_sql_btn"):
                st.session_state.current_mode = "text_to_sql"
                st.rerun()
        
        with col2:
            if st.button("📁 Chat with Files\n\nUpload files and ask questions", 
                        use_container_width=True, 
                        key="file_chat_btn"):
                st.session_state.current_mode = "file_chat"
                st.rerun()
        
        # Quick info section
        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.write("""
        This AI Assistant helps you with two main tasks:
        
        **🔍 Text-to-SQL**: Convert your natural language questions into SQL queries and execute them on your database.
        
        **📁 Chat with Files**: Upload documents (PDF, TXT, CSV, DOCX) and ask questions about their content.
        """)
    
    # Show the selected mode
    elif st.session_state.current_mode == "text_to_sql":
        show_text_to_sql()
    
    elif st.session_state.current_mode == "file_chat":
        show_file_chat()

if __name__ == "__main__":
    main()