# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
# https://github.com/smartlegionlab/
# --------------------------------------------------------
import requests
import time
from typing import Dict, List, Optional

from core.models import RepoInfo


class GitHubAPIClient:

    def __init__(self, token: str, timeout: int = 30, max_retries: int = 3):
        self.token = token
        self.timeout = timeout
        self.max_retries = max_retries
        self.base_url = 'https://api.github.com'
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'GitHub-Backup-Tools/2.0'
        })
        self.login = None
        self._rate_limit_remaining = 5000
        self._rate_limit_reset = 0

    def _check_rate_limit(self):
        if self._rate_limit_remaining < 100:
            wait_time = max(0, self._rate_limit_reset - time.time())
            if wait_time > 0:
                print(f"\n⏳ Rate limit approaching, waiting {wait_time / 60:.1f} minutes...")
                time.sleep(wait_time + 5)

    def _make_request(self, url: str) -> Optional[Dict]:
        for attempt in range(self.max_retries):
            try:
                self._check_rate_limit()

                print(f"   Attempt {attempt + 1}/{self.max_retries}...", end=' ')

                response = self.session.get(url, timeout=self.timeout)

                self._rate_limit_remaining = int(response.headers.get('X-RateLimit-Remaining', 5000))
                self._rate_limit_reset = int(response.headers.get('X-RateLimit-Reset', 0))

                if response.status_code == 200:
                    print("✅")
                    return response.json()
                elif response.status_code == 403 and 'rate limit' in response.text.lower():
                    print("⚠️ Rate limit hit")
                    reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
                    wait_time = max(0, reset_time - time.time())
                    if wait_time > 0:
                        print(f"   Waiting {wait_time / 60:.1f} minutes...")
                        time.sleep(wait_time + 5)
                else:
                    print(f"❌ HTTP {response.status_code}")
                    if response.status_code == 401:
                        return None
            except requests.exceptions.Timeout:
                print(f"⏱️ Timeout")
            except requests.exceptions.ConnectionError:
                print(f"🔌 Connection error")
            except Exception as e:
                print(f"❌ Error: {e}")

            if attempt < self.max_retries - 1:
                wait = 2 ** attempt
                print(f"   Waiting {wait}s before retry...")
                time.sleep(wait)

        return None

    def _get_paginated(self, url: str) -> List[Dict]:
        all_items = []
        page = 1

        while True:
            paginated_url = f"{url}&page={page}" if '?' in url else f"{url}?page={page}"
            data = self._make_request(paginated_url)

            if not data:
                break

            all_items.extend(data)

            if len(data) < 30:
                break

            page += 1

        return all_items

    def verify_token(self) -> bool:
        url = f"{self.base_url}/user"
        data = self._make_request(url)

        if data:
            self.login = data.get('login')
            return True
        return False

    def get_all_repos(self) -> List[RepoInfo]:
        print("\n📦 Fetching all repositories...")

        repos = []

        print("   Fetching user repositories...")
        user_repos = self._get_paginated(f"{self.base_url}/user/repos?per_page=100&type=all")
        repos.extend(user_repos)
        print(f"   ✅ Found {len(user_repos)} user repositories")

        print("\n   Fetching organization repositories...")
        orgs = self._get_paginated(f"{self.base_url}/user/orgs?per_page=100")

        for org in orgs:
            org_name = org['login']
            print(f"   Fetching {org_name} repositories...")
            org_repos = self._get_paginated(f"{self.base_url}/orgs/{org_name}/repos?per_page=100")
            repos.extend(org_repos)
            print(f"      ✅ Found {len(org_repos)} repositories")

        repo_infos = []
        for repo in repos:
            repo_infos.append(RepoInfo(
                name=repo['name'],
                full_name=repo['full_name'],
                clone_url=repo['clone_url'],
                default_branch=repo['default_branch'],
                private=repo['private'],
                pushed_at=repo['pushed_at']
            ))

        unique_repos = {r.full_name: r for r in repo_infos}.values()

        print(f"\n✅ Total unique repositories: {len(unique_repos)}")
        return list(unique_repos)
