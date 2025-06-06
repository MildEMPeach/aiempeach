#!/usr/bin/env python3
import os
import sys
import argparse
from typing import List, Dict, Any
from langchain_deepseek import ChatDeepSeek
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.callbacks import BaseCallbackHandler
from dotenv import load_dotenv

try:
    load_dotenv()
except Exception as e:
    print(f"Error loading .env file: {e}")

class StreamingCallbackHandler(BaseCallbackHandler):
    """实时流式输出回调处理器"""
    
    def __init__(self):
        self.text = ""
        self.buffer = ""
    
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        """当接收到新的token时调用"""
        try:
            # 确保token是字符串格式
            if token is not None:
                # 处理可能的编码问题
                if isinstance(token, bytes):
                    token = token.decode('utf-8', errors='ignore')
                
                # 缓冲输出以避免显示问题
                self.buffer += token
                self.text += token
                
                # 实时输出
                sys.stdout.write(token)
                sys.stdout.flush()
        except Exception as e:
            # 静默处理编码错误，避免中断流式输出
            pass
    
    def on_llm_end(self, response, **kwargs) -> None:
        """LLM响应结束时调用"""
        # 确保输出完整
        if self.buffer:
            sys.stdout.flush()
    
    def reset(self):
        """重置处理器状态"""
        self.text = ""
        self.buffer = ""

class AIEmpeach:
    def __init__(self, model: str = "deepseek-chat"):
        """初始化AI助手"""
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            print("❌ 错误: 请设置 DEEPSEEK_API_KEY 环境变量")
            sys.exit(1)
        
        self.model = model
        self.llm = ChatDeepSeek(
            model=model,
            api_key=self.api_key,
            streaming=True,
            temperature=0.7
        )
        self.conversation_history: List[Dict[str, Any]] = []
        self.streaming_handler = StreamingCallbackHandler()
        
    def add_system_message(self):
        """添加系统提示消息"""
        system_prompt = """你是一个智能的命令行助手，专门帮助用户处理各种技术问题。请遵循以下原则：
1. 提供准确、有用的信息
2. 回答要简洁明了，重点突出
3. 对于代码相关问题，提供具体的解决方案
4. 支持中文交流，语言自然流畅
5. 当用户提供文件内容或命令输出时，仔细分析并给出专业建议"""
        
        self.conversation_history.append({"role": "system", "content": system_prompt})
    
    def process_pipe_input(self, question: str = None) -> str:
        """处理管道输入"""
        if not sys.stdin.isatty():
            # 从管道读取输入
            pipe_content = sys.stdin.read().strip()
            if pipe_content:
                if question:
                    return f"以下是输入的内容：\n\n{pipe_content}\n\n问题：{question}"
                else:
                    return f"请分析以下内容：\n\n{pipe_content}"
        return question
    
    def get_response_stream(self, message: str) -> str:
        """获取流式响应"""
        # 构建消息历史
        messages = []
        
        # 添加历史消息
        for msg in self.conversation_history:
            if msg["role"] == "system":
                messages.append(SystemMessage(content=msg["content"]))
            elif msg["role"] == "human":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))
        
        # 添加当前用户消息
        messages.append(HumanMessage(content=message))
        
        # 重置流式处理器
        self.streaming_handler.reset()
        
        try:
            # 流式调用
            response = self.llm.invoke(
                messages,
                config={"callbacks": [self.streaming_handler]}
            )
            
            # 获取完整响应内容
            if hasattr(response, 'content'):
                full_response = response.content
            else:
                # 如果response没有content属性，使用流式处理器收集的文本
                full_response = self.streaming_handler.text or str(response)
            
            # 确保输出完整
            self.streaming_handler.on_llm_end(response)
            
            return full_response
            
        except KeyboardInterrupt:
            print("\n⚠️ 响应被用户中断")
            return "响应被中断"
        except Exception as e:
            error_msg = f"❌ API调用失败: {str(e)}"
            print(f"\n{error_msg}")
            return error_msg
    
    def add_to_history(self, role: str, content: str):
        """添加对话到历史记录"""
        self.conversation_history.append({"role": role, "content": content})
    
    def interactive_mode(self):
        """交互式对话模式"""
        print("🤖 AIEmpeach - 智能命令行助手")
        print(f"📡 使用模型: {self.model}")
        print("💬 开始对话吧！(输入 'exit', 'quit', 'q' 退出)")
        print("=" * 50)
        
        # 添加系统消息
        self.add_system_message()
        
        while True:
            try:
                # 获取用户输入
                user_input = input("\n💭 你: ").strip()
                
                # 检查退出命令
                if user_input.lower() in ['exit', 'quit', 'q', 'bye']:
                    print("\n👋 再见！")
                    break
                
                if not user_input:
                    continue
                
                # 添加用户消息到历史
                self.add_to_history("human", user_input)
                
                # 获取AI响应
                print(f"\n🤖 AIEmpeach: ", end='', flush=True)
                response = self.get_response_stream(user_input)
                print()  # 换行
                
                # 添加AI响应到历史
                self.add_to_history("assistant", response)
                
            except KeyboardInterrupt:
                print("\n\n👋 程序已退出")
                break
            except EOFError:
                print("\n\n👋 程序已退出")
                break

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="🤖 AIEmpeach - 基于DeepSeek API的智能命令行助手",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python aiempeach.py                    # 交互模式
  cat file.txt | python aiempeach.py -q "分析这个文件"  # 管道模式
  python aiempeach.py -m deepseek-reasoner  # 使用推理模型
        """
    )
    
    parser.add_argument(
        '-m', '--model',
        type=str,
        default='deepseek-chat',
        choices=['deepseek-chat', 'deepseek-reasoner'],
        help='选择使用的模型 (默认: deepseek-chat)'
    )
    
    args = parser.parse_args()
    
    # 创建AI助手实例
    ai = AIEmpeach(model=args.model)
    ai.interactive_mode()

if __name__ == "__main__":
    main()
