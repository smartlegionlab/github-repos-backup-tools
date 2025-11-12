import os
import shutil
import subprocess
from datetime import datetime, timezone
from typing import Dict, Any
from tools.steps.base import BaseStep
from tools.progress_bar import ProgressBar


class RepositoriesStep(BaseStep):
    def __init__(self):
        super().__init__(
            name="Repositories Operations",
            description="Fetching and cloning/updating repositories"
        )

    def execute(self, context: Dict[str, Any]) -> bool:
        print(f"🔧 {self.description}...")

        args = context.get('args', {})
        github_client = context.get('github_client')
        backup_path = context.get('backup_path')

        if not getattr(args, 'repos', False):
            print("⚠️ Repository backup not requested - skipping")
            return True

        if not github_client or not backup_path:
            print("❌ Missing required context data")
            return False

        timeout = getattr(args, 'timeout', 30)
        verbose = getattr(args, 'verbose', False)

        print("📦 Fetching repositories...")
        github_client.fetch_repositories(max_retries=3, timeout=timeout)
        repos_count = len(github_client.repositories)
        print(f"✅ Found {repos_count} repositories")

        if repos_count == 0:
            print("⚠️ No repositories to process")
            return True

        repos_target_dir = os.path.join(backup_path, "repositories")
        failed_repos = self._clone_items(repos_target_dir, github_client.repositories, "repositories", timeout, verbose)
        context['failed_repos'] = failed_repos

        self.success = True
        return True

    def _clone_items(self, target_dir: str, items: dict, item_type: str, timeout: int, verbose: bool) -> dict:
        print(f"\n📦 Processing {len(items)} {item_type}...")

        failed_dict = {}
        failed_count = 0

        if verbose:
            for name, item_data in items.items():
                print(f"\n🔍 Processing: {name}")
                success = self._process_single_item(name, item_data, target_dir, timeout)
                if not success:
                    failed_dict[name] = item_data['ssh_url']
                    failed_count += 1
        else:
            progress_bar = ProgressBar()
            for index, (name, item_data) in enumerate(items.items(), 1):
                progress_bar.update(index, len(items), failed_count, f"Processing: {name}")
                success = self._process_single_item(name, item_data, target_dir, timeout)
                if not success:
                    failed_dict[name] = item_data['ssh_url']
                    failed_count += 1

            if not failed_dict:
                progress_bar.finish(f'Cloning/updating {item_type} completed successfully!')

        if failed_dict:
            print(f"\n🔄 Retrying {len(failed_dict)} failed {item_type}...")
            failed_dict = self._retry_failed_items(failed_dict, target_dir, timeout, verbose)

        return failed_dict

    def _process_single_item(self, name: str, item_data: dict, target_dir: str, timeout: int) -> bool:
        try:
            item_path = self._create_item_path(target_dir, name)
            url = item_data['ssh_url']
            pushed_at = item_data.get('pushed_at')

            if os.path.exists(item_path):
                if pushed_at and self._needs_update(item_path, pushed_at):
                    return self._git_pull(item_path, timeout)
                else:
                    return True  # Уже актуально
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

    def _needs_update(self, repo_path: str, github_pushed_at: str) -> bool:
        try:
            local_date = self._get_local_commit_date(repo_path)
            github_date = datetime.fromisoformat(github_pushed_at.replace('Z', '+00:00'))

            local_date_utc = local_date.astimezone(timezone.utc).replace(
                tzinfo=None) if local_date.tzinfo else local_date
            github_date_utc = github_date.replace(tzinfo=None)

            time_diff = github_date_utc - local_date_utc
            return time_diff.total_seconds() > 300

        except Exception:
            return True

    def _get_local_commit_date(self, repo_path: str) -> datetime:
        try:
            git_dir = os.path.join(repo_path, '.git')
            if not os.path.exists(git_dir):
                return datetime.min

            check_result = subprocess.run(
                ['git', '-C', repo_path, 'rev-parse', '--verify', 'HEAD'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=60
            )

            if check_result.returncode != 0:
                return datetime.min

            result = subprocess.run(
                ['git', '-C', repo_path, 'show', '-s', '--format=%ci', 'HEAD'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=60
            )

            if result.returncode == 0 and result.stdout.strip():
                date_line = result.stdout.strip().split('\n')[0]
                if date_line:
                    date_str_clean = date_line.replace(' +', '+').replace(' -', '-')
                    return datetime.fromisoformat(date_str_clean)

            return datetime.min

        except Exception:
            return datetime.min

    def _git_clone(self, url: str, item_path: str, timeout: int) -> bool:
        try:
            result = subprocess.run(
                ['git', 'clone', url, item_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=timeout
            )
            return result.returncode == 0
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
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            return False
        except Exception:
            return False
