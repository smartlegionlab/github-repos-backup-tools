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
                 max_retries: int = 5):
        self.github_client = github_client
        self.username = github_client.login
        self.timeout = timeout
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
            check_result = subprocess.run(
                ['git', '-C', str(repo_path), 'rev-parse', '--verify', 'HEAD'],
                capture_output=True,
                text=True,
                timeout=10
            )

            if check_result.returncode != 0:
                return None

            result = subprocess.run(
                ['git', '-C', str(repo_path), 'log', '-1', '--format=%cI'],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0 and result.stdout.strip():
                date_line = result.stdout.strip().split('\n')[0]
                if date_line:
                    date_str_clean = date_line.replace(' +', '+').replace(' -', '-')
                    return datetime.fromisoformat(date_str_clean)
            return None

        except Exception:
            return None

    def _needs_update(self, repo_path: Path, repo: RepoInfo) -> bool:
        try:
            if not repo_path.exists() or not (repo_path / '.git').exists():
                return True

            local_date = self._get_local_commit_date(repo_path)
            if not local_date:
                return True

            github_date = datetime.fromisoformat(repo.pushed_at.replace('Z', '+00:00'))

            if local_date.tzinfo is None:
                local_date_utc = local_date.replace(tzinfo=timezone.utc)
            else:
                local_date_utc = local_date.astimezone(timezone.utc)

            github_date_utc = github_date.replace(tzinfo=timezone.utc)

            time_diff = github_date_utc - local_date_utc
            diff_seconds = time_diff.total_seconds()

            if diff_seconds <= 300:
                return False

            remote_result = subprocess.run(
                ['git', '-C', str(repo_path), 'ls-remote', 'origin', 'HEAD'],
                capture_output=True,
                text=True,
                timeout=10
            )

            if remote_result.returncode != 0:
                return True

            remote_data = remote_result.stdout.strip()
            if not remote_data:
                return True

            remote_hash = remote_data.split()[0]

            local_hash_result = subprocess.run(
                ['git', '-C', str(repo_path), 'rev-parse', 'HEAD'],
                capture_output=True,
                text=True,
                timeout=5
            )

            if local_hash_result.returncode != 0:
                return True

            local_hash = local_hash_result.stdout.strip()

            return local_hash != remote_hash

        except Exception as e:
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

            branch_result = subprocess.run(
                ['git', '-C', str(repo_path), 'rev-parse', '--abbrev-ref', 'HEAD'],
                capture_output=True,
                text=True,
                timeout=5
            )

            current_branch = branch_result.stdout.strip() if branch_result.returncode == 0 else 'master'

            pull_cmd = ['git', '-C', str(repo_path), 'pull', 'origin', current_branch]
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

            exists = repo_path.exists() and (repo_path / '.git').exists()
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
