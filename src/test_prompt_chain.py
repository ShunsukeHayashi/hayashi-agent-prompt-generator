"""
Hayashi Agent Prompt Generatorのテストスイート

このモジュールは、プロンプト生成システムの各コンポーネントをテストします：
1. 役割分析チェーン
2. プロンプト生成チェーン
3. 検証チェーン
4. 完全な生成パイプライン

各テストケースは、特定の機能を検証し、期待される出力と実際の出力を比較します。
"""

import unittest
from prompt_chain import PromptChainBuilder, Tool, AgentConfig
import os
from dotenv import load_dotenv

class TestPromptChainBuilder(unittest.TestCase):
    """
    PromptChainBuilderのテストケース集

    このテストスイートは、プロンプト生成システムの各コンポーネントが
    期待通りに動作することを確認します。

    Attributes:
        builder (PromptChainBuilder): テスト対象のビルダーインスタンス
    """

    @classmethod
    def setUpClass(cls):
        """
        テストクラスの初期化

        環境変数を読み込み、ビルダーインスタンスを作成します。
        """
        load_dotenv()
        cls.builder = PromptChainBuilder()

    def test_role_analysis_chain(self):
        """
        役割分析チェーンのテスト

        以下を検証します：
        1. ユーザー入力から適切なAgentConfigが生成されるか
        2. 必要な情報（責任、ツール、制約）が含まれているか
        3. 生成された設定が妥当な値を持つか
        """
        test_input = """
        プロジェクト管理と開発支援を行うAIエージェントが必要です。
        
        必要な機能：
        1. タスク管理（作成、更新、削除、優先順位付け）
        2. コードレビュー支援
        3. ドキュメント管理
        
        制約：セキュリティ重視、高パフォーマンス
        """
        
        result = self.builder.create_role_analysis_chain().invoke({"user_input": test_input})
        
        self.assertIsInstance(result, AgentConfig)
        self.assertTrue(len(result.responsibilities) > 0)
        self.assertTrue(len(result.tools) > 0)
        self.assertTrue(len(result.constraints) > 0)

    def test_prompt_generation_chain(self):
        """
        プロンプト生成チェーンのテスト

        以下を検証します：
        1. AgentConfigから適切なJinja2テンプレートが生成されるか
        2. 必要な要素（役割名、ツール等）が含まれているか
        3. 生成されたプロンプトが文字列形式か
        """
        test_config = AgentConfig(
            role_name="開発支援エージェント",
            responsibilities=["タスク管理", "コードレビュー"],
            principles=["効率性重視", "品質重視"],
            tools=[
                Tool(
                    name="task_manager",
                    description="タスク管理ツール",
                    parameters=[{"name": "task_id", "type": "string"}],
                    usage_format="<task_manager><task_id>123</task_id></task_manager>"
                )
            ],
            constraints=["セキュリティ重視"]
        )
        
        result = self.builder.create_prompt_generation_chain().invoke({"agent_config": str(test_config)})
        
        self.assertIsInstance(result, str)
        self.assertIn("jinja2", result.lower())
        self.assertIn("開発支援エージェント", result)
        self.assertIn("task_manager", result)

    def test_validation_chain(self):
        """
        プロンプト検証チェーンのテスト

        以下を検証します：
        1. Jinja2テンプレートの構文が正しく検証されるか
        2. 検証結果が文字列として返されるか
        3. 検証結果が空でないか
        """
        test_prompt = """
        {% import 'macros/formatting.j2' as fmt %}
        # {{ role.name }}
        
        ## 基本原則
        {% for principle in role.principles %}
        - {{ principle }}
        {% endfor %}
        """
        
        result = self.builder.create_validation_chain().invoke({"agent_prompt": test_prompt})
        
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

    def test_complete_chain(self):
        """
        完全なチェーンのテスト

        以下を検証します：
        1. ユーザー入力から完全なプロンプトが生成されるか
        2. 生成結果に必要な要素が含まれているか
        3. 各段階（設定、プロンプト、検証）の結果が含まれているか
        """
        test_input = """
        コードレビューを支援するAIエージェントが必要です。
        機能：コードの品質チェック、ベストプラクティスの提案
        制約：セキュリティとパフォーマンスを重視
        """
        
        result = self.builder.generate_prompt(test_input)
        
        self.assertIsInstance(result, dict)
        self.assertIn("agent_config", result)
        self.assertIn("agent_prompt", result)
        self.assertIn("validation_result", result)

if __name__ == '__main__':
    unittest.main() 