# 🤖 AIEmpeach

基于DeepSeek API的智能命令行助手，支持多种交互方式和文件处理功能。

## 特性

- 基于DeepSeek API的智能问答
- 流式输出，实时显示回答
- 支持文件内容读取和处理
- 支持管道输入
- 支持多种模型选择
- 中文优化的智能助手

## 快速开始

### 环境要求

- Python 3.6+
- DeepSeek API Key

### 快速安装

```bash
pip install -e .
```

### 配置API Key

创建 `.env` 文件并添加你的DeepSeek API Key：

```env
DEEPSEEK_API_KEY=your_deepseek_api_key_here
```

## 使用方法

### 基本使用

```bash
# 直接运行聊天模式
aiempeach

# 指定模型
aiempeach -m deepseek-chat
aiempeach -m deepseek-reasoner
```

### 管道输入

```bash
# 通过管道输入文件内容
cat file.txt | aiempeach

# 结合其他命令
echo "解释这段代码" | aiempeach
```

### 文件引用

在聊天过程中，你可以使用 `@file("filename")` 语法来引用文件内容：

```
😊: 请分析这个文件 @file("main.py")
```

## 命令行选项

| 选项 | 简写 | 描述 | 默认值 |
|------|------|------|--------|
| `--model` | `-m` | 选择使用的模型 | `deepseek-chat` |

### 可用模型

- `deepseek-chat`: 通用对话模型
- `deepseek-reasoner`: 推理增强模型

## 使用技巧

1. **文件分析**: 使用 `@file("path/to/file")` 语法可以让AI分析任何文本文件
2. **管道处理**: 配合Linux/Unix命令行工具，可以处理复杂的文本流
