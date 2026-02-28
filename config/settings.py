"""Configuration settings for Study Tracker."""

import json
import os
from typing import Dict, Any
from pathlib import Path


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
        }
    }

    CONFIG_FILE = "config.json"

    def __init__(self):
        """Initialize configuration."""
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default.
        
        Returns:
            Configuration dictionary
        """
        if os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, 'r') as f:
                    loaded_config = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    default = self.DEFAULT_CONFIG.copy()
                    default.update(loaded_config)
                    return default
            except Exception as e:
                print(f"Error loading config: {e}. Using defaults.")
                return self.DEFAULT_CONFIG.copy()
        
        return self.DEFAULT_CONFIG.copy()

    def save(self) -> None:
        """Save current configuration to file."""
        try:
            with open(self.CONFIG_FILE, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")

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
