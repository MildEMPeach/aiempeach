#!/usr/bin/env python3
import os
import sys
import argparse
from openai import OpenAI

def main():
    parser = argparse.ArgumentParser(description="aiempeach 工具：调用 deepseek ai 接口发送问题")
    parser.add_argument("prompt", nargs="*", help="你的提问内容")
    args = parser.parse_args()

    # 如果命令行中未传入提问内容，则提示用户输入
    if args.prompt:
        user_input = " ".join(args.prompt)
    else:
        user_input = input("请输入你的提问: ")

    # 从环境变量读取 API 密钥
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        print("错误：请先设置环境变量 DEEPSEEK_API_KEY")
        sys.exit(1)

    # 使用 deepseek 的接口地址初始化 OpenAI 客户端
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    # 调用对话 API
    response = client.chat.completions.create(
        model="deepseek-chat", # v3
        # model = "deepseek-reasoner" # r1
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": user_input},
        ],
        stream=True
    )

    # 输出 deepseek 的回复
    # print(response.choices[0].message.content) # 无法处理流式输出

    for chunk in response:
        print(chunk.choices[0].delta.content, end="", flush=True)

        
if __name__ == "__main__":
    main()
