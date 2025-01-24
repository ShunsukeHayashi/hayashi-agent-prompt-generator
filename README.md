---
title: Hayashi Agent Prompt Generator
emoji: 🤖
colorFrom: blue
colorTo: indigo
sdk: streamlit
sdk_version: 1.28.2
app_file: app.py
pinned: false
license: mit
python_version: "3.11"
---

# 🤖 Hayashi Agent System

A powerful AI agent system that provides structured prompts for different operational modes.

## 🌟 Features

- **Multiple Operation Modes**
  - Architect Mode: System design and structure
  - Ask Mode: Problem-solving and Q&A
  - Code Mode: Code generation and optimization

- **Tool Management**
  - File Operations
  - System Operations
  - Validation Tools

- **Security First**
  - Input Validation
  - Security Boundaries
  - Error Handling

## 🚀 Usage

1. Select an operation mode from the dropdown
2. View the generated prompt in either formatted or raw text format
3. Check environment information in the expandable section

## 🛠️ Technical Details

- Built with Python and Streamlit
- Uses Jinja2 for template rendering
- Configurable through YAML files

## 🔧 Configuration

The system can be configured through:
- `config/hayashi_agent_config.yaml`: Main configuration file
- `.env`: Environment variables
- Template files in `templates/` directory

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

Made with ❤️ by Hayashi

## 🔑 API Key設定

このアプリケーションを使用するには、Anthropic API Keyが必要です：

1. [Anthropic](https://www.anthropic.com/)でアカウントを作成
2. API Keyを取得
3. アプリケーションのサイドバーでAPI Keyを入力

## 🔒 セキュリティ

- API Keyはセッション内でのみ保持され、サーバーに保存されません
- CORS保護が有効
- XSRF保護が有効
- すべての通信はHTTPS経由

## 📝 入力例

```
プロジェクト管理と開発支援を行うAIエージェントが必要です。

必要な機能：
1. タスク管理（作成、更新、削除）
2. コードレビュー支援
3. ドキュメント管理

制約：セキュリティ重視
```

## 🛠️ 技術スタック

- Python 3.11
- Streamlit
- LangChain
- Anthropic Claude
- Jinja2

## 📄 ライセンス

MIT License

## デモの実行

Streamlitデモアプリケーションを使用して、プロンプト生成システムを視覚的に体験できます：

```bash
# デモアプリケーションの起動
streamlit run src/app.py
```

デモでは以下の機能を試すことができます：
- エージェントの要件をテキストで入力
- 生成されたプロンプトをリアルタイムで確認
- エージェント設定の詳細を表示
- プロンプトの検証結果を確認 