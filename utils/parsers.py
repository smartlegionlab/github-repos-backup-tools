# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# (see LICENSE for details).
# Copyright © 2025, Alexander Suvorov
# All rights reserved.
# --------------------------------------------------------
# https://github.com/smartlegionlab/
# --------------------------------------------------------
import os
import configparser


class ConfigParser:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(self._get_config_path(), encoding='utf-8')

    @staticmethod
    def _get_config_path() -> str:
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        return os.path.join(project_root, '.config.ini')

    def get_token(self) -> str:
        return self.config.get('github', 'token', fallback='')

    def get_github_login(self) -> str:
        return self.config.get('github', 'github_name', fallback='')
