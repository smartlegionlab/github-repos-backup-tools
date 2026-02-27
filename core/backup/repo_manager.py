# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
# https://github.com/smartlegionlab/
# --------------------------------------------------------
import subprocess
import shutil
import time
from pathlib import Path
from typing import List, Optional
from datetime import datetime, timezone

from core.config.settings import ProjectPaths
from core.github.api_client import GitHubAPIClient
from core.models import BackupStats, RepoInfo
from core.utils.progress import ProgressBar


class RepoManager:

    def __init__(self, github_client: GitHubAPIClient,
                 timeout: int = 30,
                 all_branches: bool = True,
                 max_retries: int = 5):
        self.github_client = github_client
        self.username = github_client.login
        self.timeout = timeout
        self.all_branches = all_branches
        self.max_retries = max_retries
        self.stats = BackupStats()

        self.user_dir = ProjectPaths.get_user_dir(self.username)
        self.repos_dir = ProjectPaths.get_repos_dir(self.username)

        self.repos_dir.mkdir(exist_ok=True, parents=True)

        print(f"\n📁 Backup location: {self.user_dir}")
        print(f"   Repositories: {self.repos_dir}")

    def _get_local_path(self, repo: RepoInfo) -> Path:
        safe_name = repo.full_name.replace('/', '_')
        return self.repos_dir / safe_name

    def _get_local_commit_date(self, repo_path: Path) -> Optional[datetime]:
        try:
            result = subprocess.run(
                ['git', '-C', str(repo_path), 'log', '-1', '--format=%cI'],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0 and result.stdout.strip():
                date_str = result.stdout.strip()
                return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        except Exception:
            pass
        return None

    def _needs_update(self, repo_path: Path, repo: RepoInfo) -> bool:
        if not repo_path.exists():
            return True

        git_dir = repo_path / '.git'
        if not git_dir.exists():
            return True

        try:
            local_date = self._get_local_commit_date(repo_path)
            if not local_date:
                return True

            github_date = datetime.fromisoformat(repo.pushed_at.replace('Z', '+00:00'))

            if local_date.tzinfo:
                local_date = local_date.astimezone(timezone.utc).replace(tzinfo=None)
            github_date = github_date.replace(tzinfo=None)

            time_diff = (github_date - local_date).total_seconds()
            return time_diff > 300

        except Exception:
            return True

    def _verify_repo_health(self, repo_path: Path) -> bool:
        try:
            if not (repo_path / '.git').exists():
                return False

            result = subprocess.run(
                ['git', '-C', str(repo_path), 'rev-parse', 'HEAD'],
                capture_output=True,
                timeout=10
            )

            return result.returncode == 0

        except Exception:
            return False

    def _clone_with_retry(self, repo_path: Path, repo: RepoInfo, retry_count: int = 0) -> bool:
        if retry_count >= self.max_retries:
            return False

        try:
            auth_url = repo.clone_url.replace('https://', f'https://oauth2:{self.github_client.token}@')

            cmd = ['git', 'clone', auth_url, str(repo_path)]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )

            if result.returncode != 0:
                if repo_path.exists():
                    shutil.rmtree(repo_path, ignore_errors=True)

                wait_time = 2 ** retry_count
                time.sleep(wait_time)
                return self._clone_with_retry(repo_path, repo, retry_count + 1)

            if self.all_branches:
                fetch_cmd = ['git', '-C', str(repo_path), 'fetch', '--all', '--tags']
                subprocess.run(fetch_cmd, timeout=self.timeout, capture_output=True)

            if not self._verify_repo_health(repo_path):
                shutil.rmtree(repo_path, ignore_errors=True)
                return self._clone_with_retry(repo_path, repo, retry_count + 1)

            return True

        except subprocess.TimeoutExpired:
            if repo_path.exists():
                shutil.rmtree(repo_path, ignore_errors=True)

            wait_time = 2 ** retry_count
            time.sleep(wait_time)
            return self._clone_with_retry(repo_path, repo, retry_count + 1)

        except Exception:
            if repo_path.exists():
                shutil.rmtree(repo_path, ignore_errors=True)
            return False

    def _update_with_retry(self, repo_path: Path, repo: RepoInfo, retry_count: int = 0) -> bool:
        if retry_count >= self.max_retries:
            return False

        try:
            fetch_cmd = ['git', '-C', str(repo_path), 'fetch', '--all', '--prune', '--tags']
            fetch_result = subprocess.run(fetch_cmd, timeout=self.timeout, capture_output=True)

            if fetch_result.returncode != 0:
                wait_time = 2 ** retry_count
                time.sleep(wait_time)
                return self._update_with_retry(repo_path, repo, retry_count + 1)

            pull_cmd = ['git', '-C', str(repo_path), 'pull', '--all']
            pull_result = subprocess.run(pull_cmd, timeout=self.timeout, capture_output=True)

            if pull_result.returncode != 0:
                wait_time = 2 ** retry_count
                time.sleep(wait_time)
                return self._update_with_retry(repo_path, repo, retry_count + 1)

            if not self._verify_repo_health(repo_path):
                shutil.rmtree(repo_path, ignore_errors=True)
                return self._clone_with_retry(repo_path, repo, 0)

            return True

        except subprocess.TimeoutExpired:
            wait_time = 2 ** retry_count
            time.sleep(wait_time)
            return self._update_with_retry(repo_path, repo, retry_count + 1)

        except Exception:
            return False

    def _count_branches(self, repo_path: Path) -> int:
        try:
            result = subprocess.run(
                ['git', '-C', str(repo_path), 'branch', '-a'],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                return len([l for l in result.stdout.split('\n') if l.strip()])
            return 0
        except Exception:
            return 0

    def process_repositories(self, repos: List[RepoInfo]) -> BackupStats:
        self.stats.start_time = datetime.now()
        self.stats.total_repos = len(repos)

        print(f"\n📂 Processing {len(repos)} repositories...")
        print(f"   Location: {self.user_dir}")
        print(f"   Repos: {self.repos_dir}\n")

        progress = ProgressBar()

        for i, repo in enumerate(repos, 1):
            repo_path = self._get_local_path(repo)

            exists = repo_path.exists()
            needs_update = self._needs_update(repo_path, repo) if exists else True

            if not exists:
                op_type = "CLONE"
            elif needs_update:
                op_type = "PULL "
            else:
                op_type = "SKIP "

            progress.update(
                i,
                self.stats.total_repos,
                self.stats.failed,
                f"{op_type} | {repo.full_name}"
            )

            if not exists:
                success = self._clone_with_retry(repo_path, repo)
                if success:
                    self.stats.cloned += 1
                else:
                    self.stats.failed += 1
                    self.stats.failed_repos.append(f"{repo.full_name} (clone)")

            elif needs_update:
                success = self._update_with_retry(repo_path, repo)
                if success:
                    self.stats.updated += 1
                else:
                    self.stats.failed += 1
                    self.stats.failed_repos.append(f"{repo.full_name} (update)")
            else:
                success = True
                self.stats.skipped += 1

            if success and repo_path.exists():
                self.stats.total_branches += self._count_branches(repo_path)

        progress.finish("Repository processing complete!")

        self.stats.end_time = datetime.now()

        return self.stats
