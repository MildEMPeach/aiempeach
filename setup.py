from setuptools import setup, find_packages

setup(
    name="aiempeach",
    version="1.0.0",
    description="基于DeepSeek API的智能命令行助手",
    py_modules=["aiempeach", "main"],
    install_requires=[
        "langchain-deepseek",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "aiempeach=main:main",
        ],
    },
    python_requires=">=3.6",
) 