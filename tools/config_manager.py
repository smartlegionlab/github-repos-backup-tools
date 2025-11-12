import json
import getpass
from pathlib import Path
from typing import Optional, Dict, Any


class ConfigManager:

    def __init__(self, app_name: str = "github_repos_backup_tools"):
        self.app_name = app_name
        self.config_dir = self._get_config_dir()
        self.token_file = self.config_dir / "github_token.json"
        self.config_file = self.config_dir / "config.json"

    def _get_config_dir(self) -> Path:
        home = Path.home()

        config_base = home / ".config"
        config_base.mkdir(exist_ok=True)

        app_config_dir = config_base / self.app_name
        app_config_dir.mkdir(exist_ok=True)

        return app_config_dir

    def ensure_config_dir_exists(self) -> bool:
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            print(f"❌ Error creating configuration directory: {e}")
            return False

    def token_exists(self) -> bool:
        return self.token_file.exists()

    @staticmethod
    def validate_token_format(token: str) -> bool:

        if not token:
            return False

        if len(token) < 10:
            return False

        if not all(c.isalnum() or c == '_' for c in token):
            return False

        return True

    def save_token(self, token: str) -> bool:
        try:
            if not self.validate_token_format(token):
                print("❌ Invalid token format")
                return False

            token_data = {
                "github_token": token,
                "created_at": self._get_current_timestamp()
            }

            with open(self.token_file, 'w', encoding='utf-8') as f:
                json.dump(token_data, f, indent=2, ensure_ascii=False)

            self.token_file.chmod(0o600)

            print("✅ The token was saved successfully.")
            return True

        except Exception as e:
            print(f"❌ Error saving token: {e}")
            return False

    def load_token(self) -> Optional[str]:
        try:
            if not self.token_exists():
                return None

            with open(self.token_file, 'r', encoding='utf-8') as f:
                token_data = json.load(f)

            token = token_data.get("github_token")
            if not token or not self.validate_token_format(token):
                print("❌ Invalid token format in file")
                return None

            return token

        except Exception as e:
            print(f"❌ Token loading error: {e}")
            return None

    def request_token_interactively(self) -> Optional[str]:
        print("\n🔑 GitHub Personal Access Token required")
        print("To create a token, go to: https://github.com/settings/tokens")
        print("Required permissions: repo, gist")
        print()

        try:
            token = getpass.getpass("Enter your GitHub token: ").strip()

            if not token:
                print("❌ The token cannot be empty")
                return None

            if not self.validate_token_format(token):
                print("❌ Invalid token format")
                return None

            return token

        except KeyboardInterrupt:
            print("\n❌ Input cancelled")
            return None
        except Exception as e:
            print(f"❌ Input error: {e}")
            return None

    def get_or_request_token(self) -> Optional[str]:
        token = self.load_token()
        if token:
            print("✅ Token found in configuration")
            return token

        print("❌ Token not found in configuration")
        token = self.request_token_interactively()

        if token and self.save_token(token):
            return token

        return None

    def save_config(self, config_data: Dict[str, Any]) -> bool:
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ Error saving configuration: {e}")
            return False

    def load_config(self) -> Dict[str, Any]:
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"❌ Configuration loading error: {e}")

        return {}

    def get_config_path(self) -> str:
        return str(self.config_dir)

    @staticmethod
    def _get_current_timestamp() -> str:
        from datetime import datetime
        return datetime.now().isoformat()
