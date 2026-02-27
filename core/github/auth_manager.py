# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
# https://github.com/smartlegionlab/
# --------------------------------------------------------
import getpass
import re
from typing import Optional

from core.config.settings import ProjectPaths, Config
from core.github.api_client import GitHubAPIClient


class GitHubAuthManager:

    @staticmethod
    def validate_token_format(token: str) -> bool:
        pattern = r'^[a-zA-Z0-9_-]{10,}$'
        return bool(token and re.match(pattern, token))

    @staticmethod
    def get_token_from_user() -> Optional[str]:
        print("\n🔑 GitHub Token Required")
        print("Get your token from: https://github.com/settings/tokens")
        print("Required permissions: repo (full control), read:org\n")

        while True:
            try:
                token = getpass.getpass("Enter GitHub token: ").strip()

                if not token:
                    print("❌ Token cannot be empty")
                    continue

                if not GitHubAuthManager.validate_token_format(token):
                    print("❌ Invalid token format")
                    continue

                return token

            except KeyboardInterrupt:
                print("\n\n❌ Operation cancelled")
                return None

    @staticmethod
    def authenticate(token: Optional[str] = None, timeout: int = 30) -> Optional[GitHubAPIClient]:
        print("\n🔐 GitHub Authentication")

        users = ProjectPaths.get_all_users()

        if users and not token:
            print(f"   Found existing user: {users[0]}")
            token = Config.load_token(users[0])
            if token:
                client = GitHubAPIClient(token, timeout=timeout)
                if client.verify_token():
                    print(f"✅ Authenticated as: {client.login}")
                    return client
                else:
                    print(f"   Token for {users[0]} is invalid, requesting new one...")

        if not token:
            token = GitHubAuthManager.get_token_from_user()
            if not token:
                return None

        client = GitHubAPIClient(token, timeout=timeout)
        if not client.verify_token():
            print("❌ Authentication failed")
            return None

        username = client.login

        ProjectPaths.ensure_user_dir(username)
        if Config.save_token(username, token):
            print(f"✅ Token saved for user: {username}")

        return client
