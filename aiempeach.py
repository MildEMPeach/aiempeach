#!/usr/bin/env python3
import os
import sys
import argparse
from openai import OpenAI


messages = [{"role": "system", "content": "你是计算机专业学生的ai助手,并且始终用中文回答问题"}]
api_key = os.getenv("DEEPSEEK_API_KEY")
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

def generate_message(user_input):
    messages.append({"role": "user", "content": user_input})

def generate_response(model="deepseek-chat"):
    return client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True
    )


def print_response(response):
    print()
    print("deepseek-v3:")
    assistantOutput = ""
    # IF stream=False
    # print(response.choices[0].message.content) 
    # IF stream=True
    for chunk in response:
        assistantOutput += chunk.choices[0].delta.content
        print(chunk.choices[0].delta.content, end='', flush=True)
    print()
    print()
    # Prepare for next query
    messages.append({"role": "assistant", "content": assistantOutput})

def main():
    # check api_key from environment
    if not api_key:
        print("错误：请先设置环境变量 DEEPSEEK_API_KEY")
        sys.exit(1)
    
    # first query
   
    if sys.stdin.isatty():
        print("What can I help you with?") 
    generate_message(sys.stdin.read().strip())
    print_response(generate_response())

    # redirect stdin
    sys.stdin.close()
    try:
        sys.stdin = open("/dev/tty")
    except FileNotFoundError:
        print("Error: /dev/tty not found")
        sys.exit(1)

    try:
        while True:
            if sys.stdin.isatty():
                print("Any other questions?")
            generate_message(sys.stdin.read().strip())
            print_response(generate_response())
    except KeyboardInterrupt:
        print()
        print("AIEMPEACH EXIT")
        
if __name__ == "__main__":
    main()
