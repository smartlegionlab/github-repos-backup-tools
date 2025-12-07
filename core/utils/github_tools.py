# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# (see LICENSE for details).
# Copyright © 2025, Alexander Suvorov
# All rights reserved.
# --------------------------------------------------------
# https://github.com/smartlegionlab/
# --------------------------------------------------------
import time
import urllib.request
import urllib.error
import json
from typing import Optional


class GitHubDataMaster:
    def __init__(self, token=None):
        self._token = token
        self.login = None
        self.repositories = {}
        self.gists = {}

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, token):
        self._token = token

    @property
    def headers(self) -> dict:
        return {'Authorization': f'token {self._token}'}

    def _make_request_with_retry(self, url: str, max_retries: int = 3, timeout: int = 30) -> Optional[dict]:
        retries = 0

        while retries < max_retries:
            current_retry = retries + 1
            print(f"   [~] Attempt {current_retry}/{max_retries} (timeout: {timeout}s)...", end=' ')

            req = urllib.request.Request(url, headers=self.headers)
            try:
                start_time = time.time()
                with urllib.request.urlopen(req, timeout=timeout) as response:
                    request_time = time.time() - start_time

                    if response.status == 200:
                        print(f"[ok] ({request_time:.1f}s)")
                        data = json.loads(response.read().decode('utf-8'))
                        return data
                    else:
                        print(f"[err] HTTP {response.status}")
                        raise Exception(f"Error: {response.status}")

            except urllib.error.HTTPError as e:
                print(f"[err] HTTP {e.code}")
                if e.code == 401:
                    return None
            except urllib.error.URLError as e:
                print(f"[err] Network: {e.reason}")
            except Exception as e:
                print(f"[err] Error: {str(e)}")

            retries += 1
            if retries < max_retries:
                wait_time = 2 ** retries
                print(f"   Waiting {wait_time}s before retry...")
                time.sleep(wait_time)

        print(f"[err] Max retries ({max_retries}) reached")
        return None

    def fetch_user_data(self, max_retries: int = 3, timeout: int = 30) -> bool:
        url = "https://api.github.com/user"
        data = self._make_request_with_retry(url, max_retries, timeout)

        if data:
            self.login = data.get('login')
            return True
        return False

    def fetch_repositories(self, max_retries: int = 3, timeout: int = 30):
        url = "https://api.github.com/user/repos"
        page = 1
        per_page = 100
        self.repositories = {}

        while True:
            paginated_url = f"{url}?page={page}&per_page={per_page}"
            data = self._make_request_with_retry(paginated_url, max_retries, timeout)

            if not data or not data:
                break

            for item in data:
                self.repositories[item['full_name']] = {
                    'ssh_url': item['ssh_url'],
                    'pushed_at': item['pushed_at']
                }
            page += 1

    def fetch_gists(self, max_retries: int = 3, timeout: int = 30):
        url = "https://api.github.com/gists"
        page = 1
        per_page = 100
        self.gists = {}

        while True:
            paginated_url = f"{url}?page={page}&per_page={per_page}"
            data = self._make_request_with_retry(paginated_url, max_retries, timeout)

            if not data or not data:
                break

            for item in data:
                self.gists[item['id']] = item['git_pull_url']
            page += 1

    def is_token_valid(self, max_retries: int = 3, timeout: int = 30) -> bool:
        url = "https://api.github.com/user"
        data = self._make_request_with_retry(url, max_retries, timeout)
        return data is not None
