from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get Groq API key
groq_api_key = os.getenv("GROQ_API_KEY")

# Initialize Groq LLM
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    groq_api_key=groq_api_key
)

# Create SQL prompt
sql_prompt = ChatPromptTemplate.from_template("""
You are an expert in writing PostgreSQL SQL queries. Convert the following natural language question into a correct SQL query.
Return ONLY the SQL code, nothing else.

Question: {question}
""")

# Parser to clean up response
parser = StrOutputParser()

# Build the LLM chain for SQL
sql_chain = sql_prompt | llm | parser

def natural_to_sql(question: str) -> str:
    """Convert a natural language question to SQL."""
    try:
        sql_query = sql_chain.invoke({"question": question})
        return sql_query.strip()
    except Exception as e:
        return f"-- Error generating SQL: {str(e)}"