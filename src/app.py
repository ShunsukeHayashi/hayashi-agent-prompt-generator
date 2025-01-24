"""
Hayashi Agent Prompt Generator - デモアプリケーション

このモジュールは、Streamlitを使用してプロンプト生成システムのデモUIを提供します。
ユーザーは入力を提供し、生成されたプロンプトと検証結果をリアルタイムで確認できます。
"""

import streamlit as st
from streamlit_ace import st_ace
from prompt_chain import PromptChainBuilder
from typing import Iterable
import json
import os
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

# Hugging Face Spaces用の環境変数設定
if os.getenv("HF_SPACE"):
    ANTHROPIC_API_KEY = os.getenv("HF_ANTHROPIC_API_KEY")
    if ANTHROPIC_API_KEY:
        os.environ["ANTHROPIC_API_KEY"] = ANTHROPIC_API_KEY

# セキュリティ設定
st.set_option('server.enableCORS', False)
st.set_option('server.enableXsrfProtection', True)
st.set_option('server.enableWebsocketCompression', True)

def init_session_state():
    """セッション状態の初期化"""
    if 'builder' not in st.session_state:
        st.session_state.builder = None
    if 'last_result' not in st.session_state:
        st.session_state.last_result = None
    if 'api_key' not in st.session_state:
        st.session_state.api_key = os.getenv("ANTHROPIC_API_KEY", "")

def initialize_builder():
    """PromptChainBuilderの初期化"""
    if st.session_state.api_key:
        os.environ["ANTHROPIC_API_KEY"] = st.session_state.api_key
        st.session_state.builder = PromptChainBuilder()
        return True
    return False

def display_api_key_input():
    """API Key入力フォームの表示"""
    with st.sidebar:
        st.subheader("🔑 API Key設定")
        api_key = st.text_input(
            "Anthropic API Key",
            value=st.session_state.api_key,
            type="password",
            help="Claude APIを使用するためのAPI Keyを入力してください"
        )
        
        if api_key != st.session_state.api_key:
            st.session_state.api_key = api_key
            st.session_state.builder = None
            st.experimental_rerun()

def display_agent_config(config):
    """エージェント設定の表示"""
    st.subheader("🔧 エージェント設定")
    
    # 基本情報
    st.write("**役割名:**", config.role_name)
    
    # 責任
    st.write("**責任:**")
    for resp in config.responsibilities:
        st.write(f"- {resp}")
    
    # 行動原則
    st.write("**行動原則:**")
    for prin in config.principles:
        st.write(f"- {prin}")
    
    # ツール
    st.write("**利用可能なツール:**")
    for tool in config.tools:
        with st.expander(f"🛠️ {tool.name}"):
            st.write("**説明:**", tool.description)
            st.write("**パラメータ:**")
            st.json(tool.parameters)
            st.write("**使用形式:**")
            st.code(tool.usage_format, language="xml")
    
    # 制約条件
    st.write("**制約条件:**")
    for const in config.constraints:
        st.write(f"- {const}")

def display_prompt(prompt):
    """生成されたプロンプトの表示"""
    st.subheader("📝 生成されたプロンプト")
    st_ace(
        value=prompt,
        language="jinja2",
        theme="monokai",
        key="prompt_editor",
        readonly=True,
        height=400
    )

def display_validation(validation):
    """検証結果の表示"""
    st.subheader("✅ 検証結果")
    st.write(validation)

def check_api_key():
    """API keyの確認"""
    if not os.getenv("ANTHROPIC_API_KEY"):
        st.error("⚠️ Anthropic API Keyが設定されていません。Hugging Face Spacesの設定でAPI Keyを追加してください。")
        return False
    return True

def main():
    """メイン関数"""
    try:
        st.set_page_config(
            page_title="Hayashi Agent Prompt Generator",
            page_icon="🤖",
            layout="wide"
        )
    except Exception:
        # ページ設定が既に行われている場合は無視
        pass
    
    init_session_state()
    display_api_key_input()
    
    st.title("🤖 Hayashi Agent Prompt Generator")
    st.write("""
    このデモでは、ユーザー入力からAIエージェントのプロンプトを動的に生成します。
    必要な機能と制約を入力してください。
    """)
    
    if not st.session_state.api_key:
        st.warning("⚠️ API Keyを入力してください。")
        return
    
    if st.session_state.builder is None and not initialize_builder():
        st.error("⚠️ PromptChainBuilderの初期化に失敗しました。")
        return
    
    # ユーザー入力
    user_input = st.text_area(
        "エージェントの要件を入力してください",
        height=200,
        placeholder="""例：
プロジェクト管理と開発支援を行うAIエージェントが必要です。
必要な機能：
1. タスク管理（作成、更新、削除）
2. コードレビュー支援
制約：セキュリティ重視"""
    )
    
    # 生成ボタン
    if st.button("プロンプトを生成", type="primary"):
        if not user_input:
            st.warning("要件を入力してください。")
            return
            
        with st.spinner("プロンプトを生成中..."):
            try:
                result = st.session_state.builder.generate_prompt(user_input)
                st.session_state.last_result = result
                st.success("プロンプトの生成が完了しました！")
            except Exception as e:
                st.error(f"エラーが発生しました: {str(e)}")
                return
    
    # 結果の表示
    if st.session_state.last_result:
        result = st.session_state.last_result
        
        # 2列レイアウト
        col1, col2 = st.columns([1, 1])
        
        with col1:
            display_agent_config(result["agent_config"])
        
        with col2:
            display_prompt(result["agent_prompt"])
            display_validation(result["validation_result"])

if __name__ == "__main__":
    main() 