# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# (see LICENSE for details).
# Copyright © 2025, Alexander Suvorov
# All rights reserved.
# --------------------------------------------------------
# https://github.com/smartlegionlab/
# --------------------------------------------------------
import os
import subprocess
from typing import Dict, Any
from core.steps.base import BaseStep


class VerificationStep(BaseStep):
    def __init__(self):
        super().__init__(
            name="✅ Verification",
            description="Verifying that all repositories and gists are properly cloned/updated"
        )

    def execute(self, context: Dict[str, Any]) -> bool:
        print(f"🔧 {self.description}...")

        args = context.get('args', {})
        backup_path = context.get('backup_path')
        github_client = context.get('github_client')

        if not backup_path or not github_client:
            print("❌ Missing required context data")
            return False

        total_success = True

        if getattr(args, 'repos', False) and github_client.repositories:
            success = self._verify_items(backup_path, "repositories", github_client.repositories, "repositories")
            if not success:
                total_success = False

        if getattr(args, 'gists', False) and github_client.gists:
            success = self._verify_items(backup_path, "gists", github_client.gists, "gists")
            if not success:
                total_success = False

        failed_repos = context.get('failed_repos', {})
        failed_gists = context.get('failed_gists', {})

        if failed_repos:
            print(f"❌ {len(failed_repos)} repositories failed to clone/update")
            total_success = False

        if failed_gists:
            print(f"❌ {len(failed_gists)} gists failed to clone/update")
            total_success = False

        if total_success:
            print("✅ All items verified successfully!")
        else:
            print("⚠️ Some items have issues - check logs above")

        self.success = total_success
        return total_success

    def _verify_items(self, backup_path: str, folder_name: str, items: dict, item_type: str) -> bool:
        target_dir = os.path.join(backup_path, folder_name)

        if not os.path.exists(target_dir):
            print(f"❌ {item_type} directory not found: {target_dir}")
            return False

        missing_items = []
        valid_items = 0

        for name, item_data in items.items():
            item_path = self._create_item_path(target_dir, name)

            if os.path.exists(item_path) and self._is_valid_git_repo(item_path):
                valid_items += 1
            else:
                missing_items.append(name)

        print(f"📊 {item_type.capitalize()} verification:")
        print(f"   Total: {len(items)}")
        print(f"   Valid: {valid_items}")
        print(f"   Missing: {len(missing_items)}")

        if missing_items:
            print(f"   Missing items: {', '.join(missing_items[:5])}" +
                  (f" ... and {len(missing_items) - 5} more" if len(missing_items) > 5 else ""))
            return False

        return True

    def _create_item_path(self, target_dir: str, item_name: str) -> str:
        item_path = os.path.normpath(os.path.join(target_dir, os.path.basename(item_name)))
        if not item_path.startswith(os.path.abspath(target_dir) + os.sep):
            raise ValueError(f"Potential path traversal attack! Blocked: {item_path}")
        return item_path

    def _is_valid_git_repo(self, repo_path: str) -> bool:
        git_dir = os.path.join(repo_path, '.git')
        if not os.path.exists(git_dir):
            return False

        try:
            result = subprocess.run(
                ['git', '-C', repo_path, 'rev-parse', '--verify', 'HEAD'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except Exception:
            return False
