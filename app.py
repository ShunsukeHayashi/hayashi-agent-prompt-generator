"""
Hayashi Agent Prompt Generator - Hugging Face Spaces Entry Point
"""

from jinja2 import Environment, FileSystemLoader
import yaml
import os
from pathlib import Path
from dotenv import load_dotenv

class HayashiAgent:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Initialize Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader('templates'),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Load configuration
        self.config = self._load_config()
        
        # Set up environment variables
        self.environment = {
            'type': os.getenv('ENVIRONMENT_TYPE', 'development'),
            'language': os.getenv('LANGUAGE', 'Japanese'),
            'security_level': os.getenv('SECURITY_LEVEL', 'high'),
            'CWD': os.getcwd(),
            'SHELL': os.environ.get('SHELL', ''),
            'OS': os.uname().sysname
        }

    def _load_config(self):
        """Load configuration from YAML file"""
        config_path = Path('config/hayashi_agent_config.yaml')
        if not config_path.exists():
            raise FileNotFoundError("Configuration file not found")
            
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            
        # Convert tools from dict to list
        tools_list = []
        for category, category_tools in config['tools'].items():
            for tool in category_tools:
                tool['category'] = category
                tools_list.append(tool)
        config['tools'] = tools_list
            
        return config

    def render_prompt(self, mode='architect'):
        """Render the prompt template for specified mode"""
        template = self.env.get_template('hayashi_agent.j2')
        
        # Prepare template variables
        template_vars = {
            'environment': self.environment,
            'operational_modes': self.config['operational_modes'],
            'tools': self.config['tools'],
            'tool_guidelines': self.config.get('tool_guidelines', []),
            'error_handling': self.config['error_handling'],
            'validation_rules': self.config['validation_rules'],
            'security_boundaries': self.config['security_boundaries'],
            'modes': [m for m in self.config['operational_modes'] if m['name'] == mode],
            'agent_name': "Hayashi Agent",
            'agent_version': self.config['version']
        }
        
        return template.render(**template_vars)

def main():
    try:
        # Initialize agent
        agent = HayashiAgent()
        
        # Render prompt for architect mode
        prompt = agent.render_prompt(mode='architect')
        
        # Print the rendered prompt
        print(prompt)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 