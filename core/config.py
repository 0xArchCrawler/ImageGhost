# configuration management
# handles user preferences, defaults, and settings

import os
import json
from pathlib import Path


class Config:
    """configuration manager for imageghost"""

    DEFAULT_CONFIG = {
        'version': '3.0',
        'gui': {
            'theme': 'arch_dark',
            'window_width': 1100,
            'window_height': 750,
            'remember_last_directory': True,
            'auto_backup_originals': False,
        },
        'scrubber': {
            'use_exiftool': True,
            'strip_steganography': True,
            'reencode_images': True,
            'default_output_quality': 95,
        },
        'crypto': {
            'default_algorithm': 'AES-256-GCM',
            'argon2_time_cost': 4,
            'argon2_memory_cost': 65536,  # 64 MB
            'argon2_parallelism': 4,
            'min_password_length': 12,
        },
        'secure_delete': {
            'default_method': 'dod',
            'verify_deletion': True,
        },
        'logging': {
            'enabled': True,
            'log_file': '~/.imageghost/imageghost.log',
            'max_log_size': 10485760,  # 10 MB
            'keep_logs': 5,
        },
        'performance': {
            'max_threads': 4,
            'chunk_size': 1048576,  # 1 MB
            'enable_caching': False,
        }
    }

    def __init__(self, config_path=None):
        if config_path is None:
            config_path = os.path.expanduser('~/.imageghost/config.json')

        self.config_path = config_path
        self.config = self.DEFAULT_CONFIG.copy()
        self.load()

    def load(self):
        """load configuration from file"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    user_config = json.load(f)
                    self._merge_config(user_config)
            except Exception as e:
                print(f"[!] failed to load config: {e}")
                print("[*] using default configuration")

    def save(self):
        """save configuration to file"""
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
            return True
        except Exception as e:
            print(f"[-] failed to save config: {e}")
            return False

    def _merge_config(self, user_config):
        """merge user config with defaults"""
        for key, value in user_config.items():
            if key in self.config:
                if isinstance(value, dict) and isinstance(self.config[key], dict):
                    self.config[key].update(value)
                else:
                    self.config[key] = value

    def get(self, section, key=None, default=None):
        """get configuration value"""
        if key is None:
            return self.config.get(section, default)

        section_config = self.config.get(section, {})
        return section_config.get(key, default)

    def set(self, section, key, value):
        """set configuration value"""
        if section not in self.config:
            self.config[section] = {}

        self.config[section][key] = value
        return self.save()

    def reset(self):
        """reset to default configuration"""
        self.config = self.DEFAULT_CONFIG.copy()
        return self.save()

    def export_config(self, export_path):
        """export configuration to specific path"""
        try:
            with open(export_path, 'w') as f:
                json.dump(self.config, f, indent=2)
            return True
        except Exception as e:
            print(f"[-] failed to export config: {e}")
            return False

    def import_config(self, import_path):
        """import configuration from file"""
        try:
            with open(import_path, 'r') as f:
                imported_config = json.load(f)
                self._merge_config(imported_config)
                return self.save()
        except Exception as e:
            print(f"[-] failed to import config: {e}")
            return False


# global config instance
_config = None

def get_config():
    """get global config instance"""
    global _config
    if _config is None:
        _config = Config()
    return _config
