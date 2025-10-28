from file_processor import FileProcessor
import os

class FileChatInterface:
    def __init__(self):
        self.processor = FileProcessor()
    
    def handle_file_upload(self):
        """Handle file upload interface"""
        print("\n📁 File Upload")
        print("Supported formats: PDF, TXT, CSV, DOCX")
        print("Enter file path or type 'back' to return to main menu")
        
        while True:
            file_path = input("\nEnter file path: ").strip()
            
            if file_path.lower() == 'back':
                break
            
            if not os.path.exists(file_path):
                print("❌ File not found. Please check the path.")
                continue
            
            try:
                # Use the new method for file paths
                result = self.processor.process_file_from_path(file_path)
                print(result)
                
            except Exception as e:
                print(f"❌ Error: {str(e)}")
    
    def chat_interface(self):
        """Chat interface for uploaded files"""
        if not self.processor.uploaded_files_info:
            print("❌ No files uploaded. Please upload files first.")
            return
        
        print(f"\n💬 Chat with {len(self.processor.uploaded_files_info)} uploaded files")
        print("Type 'back' to return to file menu or 'exit' to quit")
        
        uploaded_files = self.processor.get_uploaded_files()
        print("\n📚 Uploaded files:")
        for i, file_info in enumerate(uploaded_files, 1):
            content_preview = file_info.get('content_preview', 'No preview available')
            print(f"  {i}. {file_info['name']} ({file_info.get('size', 0)} chars)")
            print(f"     Preview: {content_preview}")
        
        while True:
            question = input("\n🤔 Your question: ").strip()
            
            if question.lower() == 'back':
                break
            elif question.lower() == 'exit':
                return 'exit'
            
            if question:
                response = self.processor.chat_with_files(question)
                print(f"\n📝 Answer: {response}")
    
    def show_file_menu(self):
        """Show file operations menu"""
        while True:
            print("\n📁 File Operations Menu")
            print("1. Upload file")
            print("2. Chat with uploaded files")
            print("3. List uploaded files")
            print("4. Clear all files")
            print("5. Back to main menu")
            
            choice = input("\nSelect option (1-5): ").strip()
            
            if choice == '1':
                self.handle_file_upload()
            elif choice == '2':
                result = self.chat_interface()
                if result == 'exit':
                    return 'exit'
            elif choice == '3':
                files = self.processor.get_uploaded_files()
                if files:
                    print("\n📚 Uploaded files:")
                    for i, file_info in enumerate(files, 1):
                        content_preview = file_info.get('content_preview', 'No preview available')
                        print(f"  {i}. {file_info['name']} ({file_info.get('size', 0)} characters)")
                        print(f"     Preview: {content_preview}")
                else:
                    print("❌ No files uploaded.")
            elif choice == '4':
                result = self.processor.clear_files()
                print(result)
            elif choice == '5':
                break
            else:
                print("❌ Invalid choice. Please select 1-5.")