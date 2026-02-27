# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
# https://github.com/smartlegionlab/
# --------------------------------------------------------
from pathlib import Path
import json
import datetime
from typing import Optional, List


class ProjectPaths:
    APP_NAME = "github_backup_repos_tools"

    @classmethod
    def get_app_dir(cls) -> Path:
        return Path.home() / cls.APP_NAME

    @classmethod
    def get_user_dir(cls, username: str) -> Path:
        return cls.get_app_dir() / username

    @classmethod
    def get_repos_dir(cls, username: str) -> Path:
        return cls.get_user_dir(username) / "repositories"

    @classmethod
    def get_config_file(cls, username: str) -> Path:
        return cls.get_user_dir(username) / "config.json"

    @classmethod
    def ensure_user_dir(cls, username: str) -> Path:
        user_dir = cls.get_user_dir(username)
        user_dir.mkdir(exist_ok=True, parents=True)
        return user_dir

    @classmethod
    def get_all_users(cls) -> List[str]:
        users = []
        app_dir = cls.get_app_dir()
        if app_dir.exists():
            for item in app_dir.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    users.append(item.name)
        return users


class Config:
    APP_NAME = 'GitHub Repositories Backup Tools'
    APP_URL = 'https://github.com/smartlegionlab/'
    APP_COPYRIGHT = 'Copyright © 2026, Alexander Suvorov'
    APP_HELP_URL = 'https://github.com/smartlegionlab/github-repos-backup-tools/'

    @classmethod
    def save_token(cls, username: str, token: str) -> bool:
        try:
            config_file = ProjectPaths.get_config_file(username)
            config = {
                "github_token": token,
                "username": username,
                "created_at": datetime.datetime.now().isoformat()
            }
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving token: {e}")
            return False

    @classmethod
    def load_token(cls, username: str) -> Optional[str]:
        try:
            config_file = ProjectPaths.get_config_file(username)
            if not config_file.exists():
                return None

            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            return config.get('github_token')
        except Exception:
            return None

    @classmethod
    def delete_token(cls, username: str) -> bool:
        try:
            config_file = ProjectPaths.get_config_file(username)
            if config_file.exists():
                config_file.unlink()
            return True
        except Exception:
            return False
