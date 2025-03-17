#!/usr/bin/env python3
import os
import sys
import argparse
from openai import OpenAI

def main():
    # parser = argparse.ArgumentParser(description="aiempeach 工具：调用 deepseek ai 接口发送问题")
    # parser.add_argument("prompt", nargs="*", help="你的提问内容")
    # args = parser.parse_args()

    # # 如果命令行中未传入提问内容，则提示用户输入
    # if args.prompt:
    #     user_input = " ".join(args.prompt)
    # else:
    #     user_input = input("请输入你的问题：")
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("错误：请先设置环境变量 DEEPSEEK_API_KEY")
        sys.exit(1)
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    messages = [{"role": "system", "content": "你是计算机学生的好助手，并且始终用中文回答问题"}]
    try:
        while True:
            assistantOuput = ""
            if sys.stdin.isatty():
                print("输入问题：(按Ctrl+D结束输入)")
            user_input = sys.stdin.read().strip()
            # print(user_input)
            messages.append({"role": "user", "content": user_input})

            print()
            print("deepseek-v3:")

            response = client.chat.completions.create(
            model="deepseek-chat", # v3
            # model = "deepseek-reasoner" # r1
            messages=messages,
            stream=True
            )

            # 处理非流式输出
            # print(response.choices[0].message.content) 

            # 处理流式输出
            for chunk in response:
                assistantOuput += chunk.choices[0].delta.content
                print(chunk.choices[0].delta.content, end="", flush=True)
            print()
            print()
            messages.append({"role": "assistant", "content": assistantOuput})
    
    except KeyboardInterrupt:
        print()
        
        
if __name__ == "__main__":
    main()
