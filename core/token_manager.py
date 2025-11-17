# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# (see LICENSE for details).
# Copyright © 2025, Alexander Suvorov
# All rights reserved.
# --------------------------------------------------------
# https://github.com/smartlegionlab/
# --------------------------------------------------------
import datetime
import getpass
import json
import re
from pathlib import Path
from typing import Optional


class TokenManager:

    def __init__(self, config_file: Path):
        self.config_file = config_file

    def get_token(self) -> Optional[str]:
        token = self._load_token()

        if token:
            return token

        return self._request_valid_token()

    def delete_config(self) -> bool:
        try:
            if not self.config_file.exists():
                print("ℹ️ Config file does not exist\n")
                return True

            self.config_file.unlink()
            print("✅ Config file deleted successfully\n")
            return True

        except Exception as e:
            print(f"❌ Error deleting config file: {e}\n")
            return False

    def _request_valid_token(self) -> Optional[str]:
        while True:
            try:
                token = getpass.getpass("Enter GitHub token: ").strip()

                if not token:
                    print("❌ Token cannot be empty\n")
                    continue

                if not self._validate_token(token):
                    print("❌ Invalid token format\n")
                    continue

                if self._save_token(token):
                    return token
                else:
                    print("❌ Failed to save token\n")
                    return None

            except KeyboardInterrupt:
                print("\n❌ Operation cancelled\n")
                return None
            except Exception as e:
                print(f"❌ Error: {e}\n")
                return None

    def _load_token(self) -> Optional[str]:
        try:
            if not self.config_file.exists():
                return None

            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)

            token = config.get('github_token', '').strip()
            return token if token and self._validate_token(token) else None

        except Exception as e:
            print(e)
            return None

    def _save_token(self, token: str) -> bool:
        try:
            config = {}
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)

            config['github_token'] = token
            config['created_at'] = datetime.datetime.now().isoformat()

            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4)

            return True

        except Exception as e:
            print(e)
            return False

    @staticmethod
    def _validate_token(token: str) -> bool:
        pattern = r'^[a-zA-Z0-9_-]{10,}$'
        return bool(token and re.match(pattern, token))
