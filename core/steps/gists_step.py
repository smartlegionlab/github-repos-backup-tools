# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# (see LICENSE for details).
# Copyright © 2025, Alexander Suvorov
# All rights reserved.
# --------------------------------------------------------
# https://github.com/smartlegionlab/
# --------------------------------------------------------
import os
import shutil
import subprocess
from typing import Dict, Any
from core.steps.base import BaseStep
from core.tools.progress_bar import ProgressBar


class GistsStep(BaseStep):
    def __init__(self):
        super().__init__(
            name="🔄 Gists Operations",
            description="Fetching and cloning/updating gists"
        )

    def execute(self, context: Dict[str, Any]) -> bool:
        print(f"🔧 {self.description}...")

        args = context.get('args', {})
        github_client = context.get('github_client')
        backup_path = context.get('backup_path')

        if not getattr(args, 'gists', False):
            print("⚠️ Gists backup not requested - skipping")
            return True

        if not github_client or not backup_path:
            print("❌ Missing required context data")
            return False

        timeout = getattr(args, 'timeout', 30)
        verbose = getattr(args, 'verbose', False)

        print("📝 Fetching gists...")
        github_client.fetch_gists(max_retries=3, timeout=timeout)
        gists_count = len(github_client.gists)
        print(f"✅ Found {gists_count} gists")

        if gists_count == 0:
            print("⚠️ No gists to process")
            return True

        gists_target_dir = os.path.join(backup_path, "gists")
        failed_gists = self._clone_items(gists_target_dir, github_client.gists, "gists", timeout, verbose)
        context['failed_gists'] = failed_gists

        self.success = True
        return True

    def _clone_items(self, target_dir: str, items: dict, item_type: str, timeout: int, verbose: bool) -> dict:
        print(f"\n📝 Processing {len(items)} {item_type}...")

        failed_dict = {}
        failed_count = 0

        if verbose:
            for name, url in items.items():
                print(f"\n🔍 Processing: {name}")
                success = self._process_single_item(name, url, target_dir, timeout)
                if not success:
                    failed_dict[name] = url
                    failed_count += 1
        else:
            progress_bar = ProgressBar()
            for index, (name, url) in enumerate(items.items(), 1):
                progress_bar.update(index, len(items), failed_count, f"Processing: {name}")
                success = self._process_single_item(name, url, target_dir, timeout)
                if not success:
                    failed_dict[name] = url
                    failed_count += 1

            if not failed_dict:
                progress_bar.finish(f'Cloning/updating {item_type} completed successfully!')

        if failed_dict:
            print(f"\n🔄 Retrying {len(failed_dict)} failed {item_type}...")
            failed_dict = self._retry_failed_items(failed_dict, target_dir, timeout, verbose)

        return failed_dict

    def _process_single_item(self, name: str, url: str, target_dir: str, timeout: int) -> bool:
        try:
            item_path = self._create_item_path(target_dir, name)

            if os.path.exists(item_path):
                return self._git_pull(item_path, timeout)
            else:
                return self._git_clone(url, item_path, timeout)

        except Exception as e:
            print(f"❌ Error processing {name}: {e}")
            return False

    def _retry_failed_items(self, failed_items: dict, target_dir: str, timeout: int, verbose: bool) -> dict:
        remaining_failed = failed_items.copy()
        total_retries = len(failed_items)

        while remaining_failed:
            current_failed = remaining_failed.copy()
            remaining_failed.clear()

            if verbose:
                print(f"\n🔄 Retry round: {len(current_failed)} repositories remaining")
                progress_bar = None
            else:
                print(f"\n🔄 Retrying {len(current_failed)} failed repositories...")
                progress_bar = ProgressBar()

            retry_failed_count = 0

            for i, (name, url) in enumerate(current_failed.items(), 1):
                if verbose:
                    print(f"🔍 Retrying: {name}")
                else:
                    current_success = total_retries - len(current_failed) + i - retry_failed_count
                    progress_bar.update(current_success, total_retries, retry_failed_count, f"Retrying: {name}")

                item_path = self._create_item_path(target_dir, name)

                if os.path.exists(item_path):
                    success = self._git_pull(item_path, timeout)
                    if not success:
                        shutil.rmtree(item_path)
                        success = self._git_clone(url, item_path, timeout)
                else:
                    success = self._git_clone(url, item_path, timeout)

                if not success:
                    remaining_failed[name] = url
                    retry_failed_count += 1

            if progress_bar and not remaining_failed:
                progress_bar.finish(f"All repositories processed successfully after retry!")

            if not remaining_failed:
                print(f"✅ All repositories processed successfully after retry")

        return remaining_failed

    def _create_item_path(self, target_dir: str, item_name: str) -> str:
        item_path = os.path.normpath(os.path.join(target_dir, os.path.basename(item_name)))
        if not item_path.startswith(os.path.abspath(target_dir) + os.sep):
            raise ValueError(f"Potential path traversal attack! Blocked: {item_path}")
        return item_path

    def _git_clone(self, url: str, item_path: str, timeout: int) -> bool:
        try:
            result = subprocess.run(
                ['git', 'clone', url, item_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=timeout
            )

            if result.returncode == 0:
                return self._verify_git_repo_health(item_path)
            return False

        except subprocess.TimeoutExpired:
            return False
        except Exception:
            return False

    def _git_pull(self, item_path: str, timeout: int) -> bool:
        try:
            result = subprocess.run(
                ['git', '-C', item_path, 'pull', 'origin', 'master'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=timeout
            )

            if result.returncode == 0:
                return self._verify_git_repo_health(item_path)
            return False

        except subprocess.TimeoutExpired:
            return False
        except Exception:
            return False

    def _verify_git_repo_health(self, repo_path: str) -> bool:
        try:
            result1 = subprocess.run(
                ['git', '-C', repo_path, 'rev-parse', '--git-dir'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=10
            )

            result2 = subprocess.run(
                ['git', '-C', repo_path, 'log', '--oneline', '-1'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=10
            )

            health_ok = result1.returncode == 0 and result2.returncode == 0

            if not health_ok:
                print(f"⚠️ Gist health check failed: {os.path.basename(repo_path)}")

            return health_ok

        except Exception as e:
            print(f"⚠️ Gist health check error {os.path.basename(repo_path)}: {e}")
            return False
