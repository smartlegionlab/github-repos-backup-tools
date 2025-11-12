# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# (see LICENSE for details).
# Copyright © 2025, Alexander Suvorov
# All rights reserved.
# --------------------------------------------------------
# https://github.com/smartlegionlab/
# --------------------------------------------------------
from typing import Dict, Any
from tools.steps.base import BaseStep
from tools.config_manager import ConfigManager


class ConfigurationStep(BaseStep):
    def __init__(self):
        super().__init__(
            name="Configuration Setup",
            description="Checking and setting up configuration directories and tokens"
        )
        self.config_manager = ConfigManager()

    def execute(self, context: Dict[str, Any]) -> bool:
        print(f"🔧 {self.description}...")

        if not self.config_manager.ensure_config_dir_exists():
            print("❌ Failed to create configuration directory")
            return False

        print(f"📁 Configuration directory: {self.config_manager.get_config_path()}")

        github_token = self.config_manager.get_or_request_token()
        if not github_token:
            print("❌ Failed to obtain token")
            return False

        context['github_token'] = github_token
        context['config_manager'] = self.config_manager

        print("✅ Token received successfully")
        self.success = True
        return True
