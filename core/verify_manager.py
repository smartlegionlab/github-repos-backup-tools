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


class VerifyManager:
    def __init__(self, github_client, backup_path, failed_repos, failed_gists, repo_flag=False, gists_flag=False):
        self.github_client = github_client
        self.backup_path = backup_path
        self.failed_repos = failed_repos or {}
        self.failed_gists = failed_gists or {}
        self.total_success = True
        self.repo_flag = repo_flag
        self.gists_flag = gists_flag

    def execute(self):

        if self.repo_flag:
            success = self._verify_items(
                backup_path=self.backup_path,
                folder_name="repositories",
                items=self.github_client.repositories,
                item_type="repositories"
            )
            if not success:
                self.total_success = False

        if self.gists_flag:
            success = self._verify_items(
                backup_path=self.backup_path,
                folder_name="gists",
                items=self.github_client.gists,
                item_type="gists"
            )
            if not success:
                self.total_success = False

        if self.failed_repos:
            print(f"❌ {len(self.failed_repos)} repositories failed to clone/update")
            self.total_success = False

        if self.failed_gists:
            print(f"❌ {len(self.failed_gists)} gists failed to clone/update")
            self.total_success = False

        if self.total_success:
            print("✅ All items verified successfully!")
        else:
            print("⚠️ Some items have issues - check logs above")
        return self.total_success


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
        except Exception as e:
            print(e)
            return False
