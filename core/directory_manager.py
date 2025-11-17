# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# (see LICENSE for details).
# Copyright © 2025, Alexander Suvorov
# All rights reserved.
# --------------------------------------------------------
# https://github.com/smartlegionlab/
# --------------------------------------------------------
from pathlib import Path
from typing import Optional


class DirectoryManager:

    @classmethod
    def get_backup_path(cls, github_login: str) -> Path:
        return Path.home() / f"{github_login}_github_backup"

    @classmethod
    def ensure_backup_structure_exists(
            cls,
            github_login: str,
            need_repos: bool = False,
            need_gists: bool = False
    ) -> Optional[Path]:
        try:
            backup_path = cls.get_backup_path(github_login)
            backup_path.mkdir(parents=True, exist_ok=True)

            if need_repos:
                repos_path = backup_path / "repositories"
                repos_path.mkdir(exist_ok=True)

            if need_gists:
                gists_path = backup_path / "gists"
                gists_path.mkdir(exist_ok=True)

            return backup_path

        except Exception as e:
            print(e)
            return None
