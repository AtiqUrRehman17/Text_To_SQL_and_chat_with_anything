from llm_chain import natural_to_sql
from db import execute_sql
from chat_with_files import FileChatInterface
from tabulate import tabulate

def text_to_sql_mode():
    """Handle Text-to-SQL functionality"""
    print("\n🔍 Text-to-SQL Mode")
    print("Type 'back' to return to main menu or 'exit' to quit\n")
    
    while True:
        question = input("Enter your question in natural language: ").strip()
        
        if question.lower() == 'back':
            break
        elif question.lower() in ["exit", "quit"]:
            return 'exit'
        
        if not question:
            continue
            
        print("\nConverting to SQL...\n")
        sql_query = natural_to_sql(question)
        print(f"🔹 Generated SQL:\n{sql_query}\n")
        
        print("Executing query...\n")
        columns, result = execute_sql(sql_query)
        if columns:
            print(tabulate(result, headers=columns, tablefmt="grid"))
        else:
            print(result)
        print("\n" + "-" * 80 + "\n")

def main():
    file_chat = FileChatInterface()
    
    print("🧠 Multi-Mode Assistant")
    print("=" * 50)
    
    while True:
        print("\n🎯 Main Menu")
        print("1. 🔍 Text-to-SQL (Database Query)")
        print("2. 📁 Chat with Files (PDF, TXT, CSV, DOCX)")
        print("3. 🚪 Exit")
        
        choice = input("\nSelect mode (1-3): ").strip()
        
        if choice == '1':
            result = text_to_sql_mode()
            if result == 'exit':
                print("Goodbye! 👋")
                break
        elif choice == '2':
            result = file_chat.show_file_menu()
            if result == 'exit':
                print("Goodbye! 👋")
                break
        elif choice == '3':
            print("Goodbye! 👋")
            break
        else:
            print("❌ Invalid choice. Please select 1-3.")

if __name__ == "__main__":
    main()