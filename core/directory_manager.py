# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# (see LICENSE for details).
# Copyright © 2025, Alexander Suvorov
# All rights reserved.
# --------------------------------------------------------
# https://github.com/smartlegionlab/
# --------------------------------------------------------
from pathlib import Path


class DirectoryManager:

    def __init__(self, github_login):
        self._github_login = github_login
        self._backup_path = None
        self._repo_path = None
        self._gists_path = None

    def run(self):
        self._backup_path = self._get_or_create_backup_path()
        self._repo_path = self._get_or_create_repo_path()
        self._gists_path = self._get_or_create_gists_path()
        return all(
            [
                self._backup_path,
                self._repo_path,
                self._gists_path
            ]
        )

    @property
    def github_login(self):
        return self._github_login

    @property
    def backup_path(self):
        return self._backup_path

    @property
    def repo_path(self):
        return self._repo_path

    @property
    def gists_path(self):
        return self._gists_path

    def _get_or_create_backup_path(self):
        try:
            backup_path = Path.home() / f"{self._github_login}_github_backup"
            backup_path.mkdir(parents=True, exist_ok=True)
            return backup_path
        except Exception as e:
            print(e)
            return None

    def _get_or_create_repo_path(self):
        try:
            repos_path = self._backup_path / "repositories"
            repos_path.mkdir(exist_ok=True)
            return repos_path
        except Exception as e:
            print(e)
            return None

    def _get_or_create_gists_path(self):
        try:
            gists_path = self._backup_path / "gists"
            gists_path.mkdir(exist_ok=True)
            return gists_path
        except Exception as e:
            print(e)
            return None
