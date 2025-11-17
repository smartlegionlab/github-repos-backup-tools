# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# (see LICENSE for details).
# Copyright © 2025, Alexander Suvorov
# All rights reserved.
# --------------------------------------------------------
# https://github.com/smartlegionlab/
# --------------------------------------------------------
import datetime
import json
from pathlib import Path
from typing import Optional


class Config:
    app_name = 'Github Repositories Backup Tools'
    app_url = 'https://github.com/smartlegionlab/'
    app_copyright = 'Copyright © 2025, Alexander Suvorov'
    app_help_url = 'https://github.com/smartlegionlab/github-repos-backup-tools/'


class ConfigPathManager:

    @classmethod
    def get_config_path(cls, dir_name: str = "github_repos_backup_tools") -> Path:
        return Path.home() / ".config" / dir_name / "github_token.json"

    @classmethod
    def ensure_config_exists(cls, dir_name: str = "github_repos_backup_tools") -> Optional[Path]:
        try:
            config_file = cls.get_config_path(dir_name)

            config_file.parent.mkdir(parents=True, exist_ok=True)

            if not config_file.exists():
                cls._create_default_config(config_file)

            return config_file

        except Exception as e:
            print(f"Error creating config: {e}")
            return None

    @classmethod
    def _create_default_config(cls, config_path: Path) -> None:
        default_config = {
            "github_token": "",
            "created_at": datetime.datetime.now().isoformat()
        }

        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=4, ensure_ascii=False)
