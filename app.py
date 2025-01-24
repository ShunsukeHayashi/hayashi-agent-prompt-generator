"""
Hayashi Agent Prompt Generator - Hugging Face Spaces Entry Point
"""

import sys
import os

# srcディレクトリをPythonパスに追加
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

# アプリケーションのインポートと実行
from src.app import main

if __name__ == "__main__":
    main() 