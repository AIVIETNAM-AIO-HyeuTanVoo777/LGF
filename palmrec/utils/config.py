import yaml
import os

class Config(dict):
    """Configuration class that allows dot-notation access."""
    def __init__(self, data=None):
        super().__init__()
        if data:
            for k, v in data.items():
                if isinstance(v, dict):
                    self[k] = Config(v)
                else:
                    self[k] = v

    def __getattr__(self, name):
        if name in self:
            return self[name]
        raise AttributeError(f"Configuration has no attribute: {name}")

    def __setattr__(self, name, value):
        self[name] = value

def load_config(config_path: str) -> Config:
    """Load configuration from a YAML file."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")
    with open(config_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return Config(data)
