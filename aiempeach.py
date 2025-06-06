import sys
from langchain_deepseek import ChatDeepSeek
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from typing import List, Any
import re
import os

class AIEmpeach:
    def __init__(self, api_key: str, model: str = "deepseek-chat"):
        """Initialize the AIEmpeach class"""

        # Initialize the API key
        self.api_key = api_key
        
        # Read the model from the environment variable
        self.model = model
        
        # Initialize the LLM
        self.llm = ChatDeepSeek(
            model = self.model,
            api_key = self.api_key,
            streaming = True
        )

        # Initialize the conversation history
        self.conversation_history: List[Any]= []

        # Initialize the system message
        system_prompt = """
        You are a helpful assistant named aiempeach, and you will always answer in Chinese.
        """
        try:
            self.add_to_conversation_history("system", system_prompt)
        except Exception as e:
            print(f"Error adding system message: {e}")
    
    def add_to_conversation_history(self, role: str, content: str):
        if role == "system":
            self.conversation_history.append(SystemMessage(content=content))
        elif role == "human":
            self.conversation_history.append(HumanMessage(content=content))
        elif role == "assistant":
            self.conversation_history.append(AIMessage(content=content))
        else:
            raise ValueError(f"Invalid role: {role}")

    def chat(self):
        """Chat with the llm"""
        print("🤖 aiempeach")
        print(f"📡 Model in use: {self.model}")
        print("💬 And Let's chat!(Type 'exit', 'quit', 'q' to quit)")
        print("=" * 50)

        input_from_pipe = ""
        if not sys.stdin.isatty():
            input_from_pipe = sys.stdin.read().strip()
            print("Detect Contents from the pipe...")
            # Redirect standard input from the terminal
            sys.stdin = open("/dev/tty", 'r')
        
        while True:
            try:
                user_input = input("\n😊: ").strip()

                # If there is any input from the pipe, add the input from the pipe to the user input.
                if input_from_pipe:
                    user_input += input_from_pipe
                    input_from_pipe = ""

                # Check if the user input is empty
                if not user_input:
                    continue
                
                # Substitute @file("filename") for contents of file
                user_input = self.process_file_input(user_input)
                # print(user_input)

                print("\n🤖: ", end = "")
                # Check if the user input is exit, quit, q
                if user_input.lower() in ['exit', 'quit', 'q']:
                    print("Bye!")
                    break
                
                self.add_to_conversation_history("human", user_input)
                response_content = self.get_content_and_print_stream()
                self.add_to_conversation_history("assistant", response_content)

            except KeyboardInterrupt:
                print("Bye!")
                break
            except EOFError:
                print("EOFError, Bye!")
                break
    
    def process_file_input(self, user_input):
        """Deal with the file input form @file('filename') or @file("filename")"""
        file_pattern = r"@file\(['\"]([^'\"]+)['\"]\)"
        file_list = []

        def replace_file_function(match):
            filepath = match.group(1)
            file_list.append(filepath)
            return filepath

        user_input = re.sub(file_pattern, replace_file_function, user_input)

        for filepath in file_list:
            user_input += self.read_file_content(filepath)

        return user_input

    def read_file_content(self, filepath):
        if not os.path.isabs(filepath):
            filepath = os.path.join(os.getcwd(), filepath)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            # print(f"\n\nThe contents of the file {os.path.basename(filepath)}:\n{content}\n")
            return f"\n\nThe contents of the file {os.path.basename(filepath)}:\n{content}\n"
        

    def get_content_and_print_stream(self):
        """Get and Print the content from the LLM"""
        print("", end="", flush=True)
        response_content = ""
        for chunk in self.llm.stream(self.conversation_history):
            if chunk.content:
                print(chunk.content, end="", flush=True)
            response_content += chunk.content
        return response_content
