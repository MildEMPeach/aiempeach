from aiempeach import AIEmpeach
from dotenv import load_dotenv
import os

try:
    load_dotenv()
except Exception as e:
    print(f"Error load .env file")

def main():
    aiempeach = AIEmpeach(api_key=os.getenv("DEEPSEEK_API_KEY"))
    aiempeach.chat()

if __name__ == "__main__":
    main()