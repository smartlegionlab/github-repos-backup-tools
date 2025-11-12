# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# (see LICENSE for details).
# Copyright © 2025, Alexander Suvorov
# All rights reserved.
# --------------------------------------------------------
# https://github.com/smartlegionlab/
# --------------------------------------------------------
import os
from typing import Dict, Any
from tools.steps.base import BaseStep


class DirectorySetupStep(BaseStep):
    def __init__(self):
        super().__init__(
            name="Directory Setup",
            description="Creating backup directory structure"
        )

    def execute(self, context: Dict[str, Any]) -> bool:
        print(f"🔧 {self.description}...")

        args = context.get('args', {})
        github_login = context.get('github_login')

        if not github_login:
            print("❌ No GitHub login found in context")
            return False

        backup_path = self._create_main_backup_directory(github_login)
        if not backup_path:
            return False

        success = self._create_subdirectories(backup_path, args)
        if not success:
            return False

        context['backup_path'] = backup_path
        self.success = True
        return True

    def _create_main_backup_directory(self, login: str) -> str:
        home_directory = os.path.expanduser('~')
        backup_path = os.path.join(home_directory, f'{login}_github_backup')

        try:
            os.makedirs(backup_path, exist_ok=True)
            print(f"📁 Main backup directory: {backup_path}")
            return backup_path
        except Exception as e:
            print(f"❌ Failed to create backup directory: {e}")
            return None

    def _create_subdirectories(self, backup_path: str, args) -> bool:
        directories_to_create = []

        if getattr(args, 'repos', False):
            directories_to_create.append("repositories")

        if getattr(args, 'gists', False):
            directories_to_create.append("gists")

        if not directories_to_create:
            print("⚠️ No backup operations selected - no subdirectories created")
            return True

        print("📂 Creating subdirectories:")
        for directory in directories_to_create:
            dir_path = os.path.join(backup_path, directory)
            try:
                os.makedirs(dir_path, exist_ok=True)
                print(f"   ✅ {directory}/")
            except Exception as e:
                print(f"   ❌ Failed to create {directory}/: {e}")
                return False

        return True
