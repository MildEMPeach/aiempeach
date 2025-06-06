from aiempeach import AIEmpeach
from dotenv import load_dotenv
import argparse
import os

try:
    load_dotenv()
except Exception as e:
    print(f"Error load .env file")

def main():
    parser = argparse.ArgumentParser(
        description="🤖 AIEmpeach - 基于DeepSeek API的智能命令行助手"
    )
    
    parser.add_argument(
        '-m', '--model',
        type=str,
        default='deepseek-chat',
        choices=['deepseek-chat', 'deepseek-reasoner'],
        help='选择使用的模型 (默认: deepseek-chat)'
    )

    args = parser.parse_args()
    aiempeach = AIEmpeach(api_key=os.getenv("DEEPSEEK_API_KEY"), model=args.model)
    aiempeach.chat()

if __name__ == "__main__":
    main()