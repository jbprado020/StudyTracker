"""Configuration settings for Study Tracker."""

import json
from typing import Dict, Any

from utils.paths import project_path


class Config:
    """Application configuration management."""

    DEFAULT_CONFIG = {
        "app_name": "Pradofy Study Tracker",
        "database_path": "study_sessions.db",
        "window_width": 900,
        "window_height": 600,
        "window_x": 100,
        "window_y": 100,
        "theme": "light",
        "colors": {
            "primary": "#2563eb",
            "secondary": "#60a5fa",
            "success": "#10b981",
            "danger": "#ef4444",
            "warning": "#f59e0b",
            "background": "#f5f7fa",
            "text": "#1e293b"
        },
        "features": {
            "enable_notifications": False,
            "enable_dark_mode": False,
            "auto_save_interval": 300,
            "export_auto_timestamp": True
        },
        "accessibility": {
            "high_contrast": False,
            "large_text": False,
            "base_font_size": 13
        }
    }

    CONFIG_FILE = project_path("config.json")

    def __init__(self):
        """Initialize configuration."""
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default.
        
        Returns:
            Configuration dictionary
        """
        if self.CONFIG_FILE.exists():
            try:
                with open(self.CONFIG_FILE, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    return self._merge_defaults(self.DEFAULT_CONFIG, loaded_config)
            except Exception as e:
                print(f"Error loading config: {e}. Using defaults.")
                return self.DEFAULT_CONFIG.copy()
        
        return self.DEFAULT_CONFIG.copy()

    def save(self) -> None:
        """Save current configuration to file."""
        try:
            self.CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(self.CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")

    def _merge_defaults(self, defaults: Dict[str, Any], loaded: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively merge loaded settings into defaults."""
        merged = defaults.copy()
        for key, value in loaded.items():
            if isinstance(value, dict) and isinstance(merged.get(key), dict):
                merged[key] = self._merge_defaults(merged[key], value)
            else:
                merged[key] = value
        return merged

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value.
        
        Args:
            key: Configuration key (supports dot notation: "colors.primary")
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default

        return value if value is not None else default

    def set(self, key: str, value: Any) -> None:
        """Set configuration value.
        
        Args:
            key: Configuration key (supports dot notation: "colors.primary")
            value: Value to set
        """
        keys = key.split('.')
        config = self.config

        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        config[keys[-1]] = value
        self.save()

    def get_all(self) -> Dict[str, Any]:
        """Get entire configuration.
        
        Returns:
            Complete configuration dictionary
        """
        return self.config.copy()

    def reset_to_defaults(self) -> None:
        """Reset configuration to defaults."""
        self.config = self.DEFAULT_CONFIG.copy()
        self.save()
