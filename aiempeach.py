import sys
import os
from langchain_deepseek import ChatDeepSeek
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from typing import List, Any

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
            api_key = self.api_key
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

        while True:
            try:
                
                user_input = input("\n😊: ").strip()
                
                # Check if the user input is empty
                if not user_input:
                    continue
                
                print("\n🤖: ", end = "")

                # Check if the user input is exit, quit, q
                if user_input.lower() in ['exit', 'quit', 'q']:
                    print("Bye!")
                    break
                
                self.add_to_conversation_history("human", user_input)
                response = self.get_response_stream()
                self.add_to_conversation_history("assistant", response.content)
                
                print(response.content)


            except KeyboardInterrupt:
                break
            except EOFError:
                break
                
                



    def get_response_stream(self):
        """Get and Print the response from the LLM"""
        response = self.llm.invoke(self.conversation_history)
        return response
