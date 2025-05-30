# 🤖 AIEmpeach

一个基于 DeepSeek API 的智能命令行助手，让 AI 成为你终端中的得力伙伴。

## ✨ 功能特点

- 🗣️ **多轮对话** - 支持连续提问，保持上下文记忆
- 🔄 **管道支持** - 无缝集成 Unix 管道，分析文件内容或命令输出
- 🧠 **模型选择** - 支持 DeepSeek Chat 和 DeepSeek Reasoner 模型
- 🌊 **流式输出** - 实时显示 AI 回复，体验更流畅
- 🇨🇳 **中文优化** - 专为中文用户设计，回答更贴合国内使用习惯

## 🚀 快速开始

### 前置要求

- Python 3.6+
- DeepSeek API Key

### 安装依赖

```bash
pip install openai
```

### 配置 API Key

设置环境变量：

```bash
# Linux/macOS
export DEEPSEEK_API_KEY="your_api_key_here"

```

## 💻 使用方法

### 基础对话

```bash
python aiempeach.py
```

直接启动交互式对话模式。

### 管道模式

分析文件内容：
```bash
cat your_file.txt | python aiempeach.py -q "请分析这个文件的内容"
```

分析命令输出：
```bash
ls -la | python aiempeach.py -q "解释这些文件的用途"
```

检查代码：
```bash
cat script.py | python aiempeach.py -q "这段代码有什么问题吗？"
```

### 模型选择

使用推理模型：
```bash
python aiempeach.py -m deepseek-reasoner
```

## 📖 命令行参数

| 参数 | 简写 | 描述 | 默认值 |
|------|------|------|--------|
| `--question` | `-q` | 附加问题（配合管道使用） | 无 |
| `--model` | `-m` | 选择模型 | `deepseek-chat` |

### 可用模型

- `deepseek-chat` - 通用对话模型，响应速度快
- `deepseek-reasoner` - 推理模型，逻辑分析能力更强

## 🎯 使用场景

- **代码审查**: 快速分析代码质量和潜在问题
- **日志分析**: 解读系统日志和错误信息
- **文档理解**: 快速理解技术文档和配置文件
- **学习助手**: 解答编程和技术问题
- **数据分析**: 分析结构化数据和报告

## 🔧 开发状态

### 已完成功能 ✅
- [x] 多轮对话支持
- [x] 管道输入处理 (`-q` 参数)
- [x] 模型选择功能 (`-m` 参数)

### 计划中功能 🚧
- [ ] 多轮对话中的文件读取
- [ ] 修复重定向输出的 stdout 重置问题

## ⚠️ 注意事项

1. 确保已正确设置 `DEEPSEEK_API_KEY` 环境变量
2. 网络连接需要能够访问 DeepSeek API
3. 使用 `Ctrl+C` 可以随时退出程序

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来帮助改进这个项目！


---

> 💡 **提示**: 将 `aiempeach.py` 添加到系统 PATH 中，就可以在任何地方直接使用 `aiempeach` 命令了！
