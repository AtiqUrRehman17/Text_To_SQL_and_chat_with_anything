from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import sys

# Load environment variables
load_dotenv()

# Build DATABASE_URL dynamically from .env variables
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
    print("❌ ERROR: One or more database environment variables are missing.")
    print("Please make sure your .env file includes:")
    print("DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME")
    sys.exit(1)

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create engine
try:
    engine = create_engine(DATABASE_URL)
except Exception as e:
    print(f"❌ Error creating engine: {e}")
    sys.exit(1)

def execute_sql(query: str):
    """Execute SQL query and return results or error message."""
    with engine.connect() as conn:
        try:
            result = conn.execute(text(query))
            if result.returns_rows:
                rows = result.fetchall()
                columns = result.keys()
                return columns, rows
            else:
                return None, "✅ Query executed successfully (no returned rows)."
        except Exception as e:
            return None, f"❌ Error executing query: {str(e)}"
