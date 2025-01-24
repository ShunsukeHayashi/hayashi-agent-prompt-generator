from jinja2 import Environment, FileSystemLoader
import yaml
import os
import logging
from typing import Dict, Any
from prompt_chain import PromptChainBuilder, Tool

# ロギングの設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class HayashiAgent:
    def __init__(self, config_path: str, tools_config_path: str, templates_path: str):
        """
        Hayashiエージェントの初期化
        
        Args:
            config_path (str): 設定ファイルのパス
            tools_config_path (str): ツール設定ファイルのパス
            templates_path (str): テンプレートディレクトリのパス
        """
        self.config = self._load_config(config_path)
        self.tools_config = self._load_config(tools_config_path)
        self.env = Environment(loader=FileSystemLoader(templates_path))
        self.prompt_builder = PromptChainBuilder()
        self.initialize_environment()
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """
        設定ファイルを読み込む
        
        Args:
            config_path (str): 設定ファイルのパス
            
        Returns:
            Dict[str, Any]: 設定データ
        """
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"設定ファイルの読み込みに失敗: {e}")
            raise
            
    def initialize_environment(self):
        """環境の初期化"""
        logger.info("環境を初期化中...")
        self.config['environment']['cwd'] = os.getcwd()
        
        # ツール設定の追加
        if 'tools' in self.tools_config:
            tools = []
            for tool_config in self.tools_config['tools']:
                tool = Tool(
                    name=tool_config['name'],
                    description=tool_config['description'],
                    parameters=tool_config['parameters'],
                    usage_format=tool_config['usage_format']
                )
                tools.append(tool)
            self.config['tools'] = tools
        
    def generate_dynamic_prompt(self, user_input: str) -> Dict[str, Any]:
        """
        動的プロンプトを生成
        
        Args:
            user_input (str): ユーザーからの入力
            
        Returns:
            Dict[str, Any]: 生成されたプロンプトと検証結果
        """
        return self.prompt_builder.generate_prompt(user_input)
        
    def render_prompt(self) -> str:
        """
        プロンプトをレンダリング
        
        Returns:
            str: レンダリングされたプロンプト
        """
        try:
            template = self.env.get_template('hayashi_agent.j2')
            return template.render(**self.config)
        except Exception as e:
            logger.error(f"プロンプトのレンダリングに失敗: {e}")
            raise
            
    def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Any:
        """
        ツールを実行
        
        Args:
            tool_name (str): ツール名
            parameters (Dict[str, Any]): パラメータ
            
        Returns:
            Any: 実行結果
        """
        logger.info(f"ツール実行: {tool_name}")
        try:
            # ツールの実行ロジックをここに実装
            pass
        except Exception as e:
            logger.error(f"ツール実行エラー: {e}")
            raise
            
    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """
        入力データを検証
        
        Args:
            input_data (Dict[str, Any]): 検証する入力データ
            
        Returns:
            bool: 検証結果
        """
        # 入力検証ロジックをここに実装
        return True

def main():
    """メイン実行関数"""
    try:
        # エージェントの初期化
        agent = HayashiAgent(
            config_path='config/hayashi_agent_config.yaml',
            tools_config_path='config/tools_config.yaml',
            templates_path='templates'
        )
        
        # ユーザー入力の例
        user_input = """
        タスク管理と進捗報告を行うエージェントが必要です。
        以下の機能が必要です：
        1. タスクの追加、更新、削除
        2. 進捗状況の追跡
        3. 定期的なレポート生成
        4. チーム間のコミュニケーション支援
        """
        
        # 動的プロンプトの生成
        result = agent.generate_dynamic_prompt(user_input)
        
        # 結果の出力
        print("\n=== 生成されたエージェント設定 ===")
        print(result["agent_config"])
        print("\n=== 生成されたプロンプト ===")
        print(result["agent_prompt"])
        print("\n=== 検証結果 ===")
        print(result["validation_result"])
        
    except Exception as e:
        logger.error(f"実行エラー: {e}")
        raise

if __name__ == "__main__":
    main() 