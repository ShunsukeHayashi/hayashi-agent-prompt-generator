"""
Hayashi Agent Prompt Generator

このモジュールは、動的なプロンプト生成システムを提供します。
Jinja2テンプレートとLangchainを使用して、柔軟で再利用可能なAIエージェントのプロンプトを生成します。

主な機能:
- 役割分析: ユーザー入力からエージェントの役割とツールを分析
- プロンプト生成: Jinja2テンプレートを使用した動的なプロンプト生成
- 検証: 生成されたプロンプトの構文と整合性の検証

使用例:
    >>> from prompt_chain import PromptChainBuilder
    >>> builder = PromptChainBuilder()
    >>> result = builder.generate_prompt("タスク管理エージェントが必要です")
    >>> print(result["agent_prompt"])

注意:
    - 環境変数ANTHROPIC_API_KEYが必要です
    - Python 3.8以上が必要です
"""

from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence, RunnableLambda
from langchain_anthropic import ChatAnthropic
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List, Dict, Any
import os
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

class Tool(BaseModel):
    """
    ツール定義の構造を表すモデル

    Attributes:
        name (str): ツールの名前
        description (str): ツールの説明
        parameters (List[Dict[str, str]]): ツールのパラメータリスト
        usage_format (str): ツールの使用形式（XML形式）
    """
    name: str = Field(description="ツールの名前")
    description: str = Field(description="ツールの説明")
    parameters: List[Dict[str, str]] = Field(description="ツールのパラメータリスト")
    usage_format: str = Field(description="ツールの使用形式")

class AgentConfig(BaseModel):
    """
    エージェント設定の構造を定義するモデル

    Attributes:
        role_name (str): エージェントの役割名
        responsibilities (List[str]): エージェントの責任リスト
        principles (List[str]): エージェントの行動原則
        tools (List[Tool]): 利用可能なツール
        constraints (List[str]): 制約条件
    """
    role_name: str = Field(description="エージェントの役割名")
    responsibilities: List[str] = Field(description="エージェントの責任リスト")
    principles: List[str] = Field(description="エージェントの行動原則")
    tools: List[Tool] = Field(description="利用可能なツール")
    constraints: List[str] = Field(description="制約条件")

class PromptChainBuilder:
    """
    プロンプトチェーンを構築するためのビルダークラス

    このクラスは、3つの主要なチェーンを組み合わせてプロンプトを生成します：
    1. 役割分析チェーン
    2. プロンプト生成チェーン
    3. 検証チェーン

    Attributes:
        llm: 言語モデル（Claude 3.5 Sonnet）
        config_parser: AgentConfig用のPydanticパーサー
    """

    def __init__(self):
        """
        プロンプトチェーンビルダーの初期化

        環境変数ANTHROPIC_API_KEYが必要です。
        """
        self.llm = ChatAnthropic(
            temperature=0.7,
            model="claude-3-sonnet-20240229",
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
        )
        self.config_parser = PydanticOutputParser(pydantic_object=AgentConfig)

    def create_role_analysis_chain(self) -> RunnableSequence:
        """
        役割分析チェーンを作成

        ユーザー入力を分析し、エージェントの設定を生成します。

        Returns:
            RunnableSequence: 役割分析チェーン
        """
        template = """
        ユーザーの入力から適切なエージェントの役割とツールを分析してください。

        入力: {user_input}

        以下の要素を含めて出力してください：
        1. エージェントの役割と責任
        2. 必要なツール（各ツールには名前、説明、パラメータ、使用形式を含める）
        3. 制約条件と行動原則

        出力形式：
        {format_instructions}
        """
        
        prompt = PromptTemplate(
            template=template,
            input_variables=["user_input"],
            partial_variables={"format_instructions": self.config_parser.get_format_instructions()}
        )
        
        return prompt | self.llm | self.config_parser

    def create_prompt_generation_chain(self) -> RunnableSequence:
        """
        プロンプト生成チェーンを作成

        AgentConfigに基づいてJinja2テンプレート形式のプロンプトを生成します。

        Returns:
            RunnableSequence: プロンプト生成チェーン
        """
        template = """
        以下の設定に基づいて、Jinja2テンプレート形式でHayashiエージェントのプロンプトを生成してください。

        設定:
        {agent_config}

        以下の構造で出力してください：

        ```jinja2
        {{{{ import 'macros/formatting.j2' as fmt }}}}
        {{{{ import 'macros/tools.j2' as tools }}}}
        {{{{ import 'macros/validation.j2' as validate }}}}

        {{# エージェント定義 #}}
        ◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢
        # {{ role.name }}
        Version: {{ version }}

        ## 基本原則
        {{{{ for principle in role.principles }}}}
        - {{ principle }}
        {{{{ endfor }}}}
        ◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢◤◢

        ## システムロール
        あなたは、{{ role.name }}として以下の責任を持ちます：

        {{{{ for responsibility in role.responsibilities }}}}
        - {{ responsibility }}
        {{{{ endfor }}}}

        ## 利用可能なツール
        {{{{ for tool in tools }}}}
        ### {{ tool.name }}
        {{ tool.description }}
        
        使用形式:
        ```
        {{ tool.usage_format }}
        ```
        {{{{ endfor }}}}

        ## 制約条件
        {{{{ for constraint in constraints }}}}
        - {{ constraint }}
        {{{{ endfor }}}}
        ```
        """
        
        prompt = PromptTemplate(
            template=template,
            input_variables=["agent_config"]
        )
        
        chain = prompt | self.llm
        return chain | RunnableLambda(lambda x: str(x.content if hasattr(x, 'content') else x))

    def create_validation_chain(self) -> RunnableSequence:
        """
        プロンプト検証チェーンを作成

        生成されたプロンプトの構文と整合性を検証します。

        Returns:
            RunnableSequence: 検証チェーン
        """
        template = """
        生成されたJinja2テンプレート形式のプロンプトを検証してください。

        プロンプト:
        {agent_prompt}

        以下の観点で検証し、具体的な改善点を指摘してください：
        1. Jinja2テンプレート構文の正確性
        2. マクロの適切な使用
        3. 変数の定義と参照の整合性
        4. 制御構文の正しい使用
        5. 出力フォーマットの遵守

        検証結果を文字列として返してください。
        """
        
        prompt = PromptTemplate(
            template=template,
            input_variables=["agent_prompt"]
        )
        
        chain = prompt | self.llm
        return chain | RunnableLambda(lambda x: str(x.content if hasattr(x, 'content') else x))

    def build_chain(self) -> RunnableSequence:
        """
        完全なプロンプトチェーンを構築

        3つのチェーンを組み合わせて完全なプロンプト生成パイプラインを作成します。

        Returns:
            RunnableSequence: 完全なプロンプトチェーン
        """
        role_chain = self.create_role_analysis_chain()
        prompt_chain = self.create_prompt_generation_chain()
        validation_chain = self.create_validation_chain()
        
        def combine_outputs(inputs: Dict[str, Any]) -> Dict[str, Any]:
            agent_config = role_chain.invoke(inputs)
            agent_prompt = prompt_chain.invoke({"agent_config": agent_config})
            validation_result = validation_chain.invoke({"agent_prompt": agent_prompt})
            return {
                "agent_config": agent_config,
                "agent_prompt": agent_prompt,
                "validation_result": validation_result
            }
        
        return RunnableLambda(combine_outputs)

    def generate_prompt(self, user_input: str) -> Dict[str, Any]:
        """
        プロンプトの生成と検証を実行

        Args:
            user_input (str): ユーザーからの入力テキスト

        Returns:
            Dict[str, Any]: {
                "agent_config": AgentConfig,
                "agent_prompt": str,
                "validation_result": str
            }
        """
        chain = self.build_chain()
        return chain.invoke({"user_input": user_input})