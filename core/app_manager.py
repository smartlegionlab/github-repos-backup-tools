# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
# https://github.com/smartlegionlab/
# --------------------------------------------------------
import json
import signal
import sys
from datetime import datetime

from core.backup.archive_manager import ArchiveManager
from core.backup.repo_manager import RepoManager
from core.config.args_manager import ArgumentsManager
from core.config.settings import Config, ProjectPaths
from core.github.api_client import GitHubAPIClient
from core.github.auth_manager import GitHubAuthManager
from core.models import BackupStats
from core.reports.report_generator import ReportGenerator
from core.utils.network import NetworkChecker
from core.utils.printer import SmartPrinter


class AppManager:
    def __init__(self):
        self.printer = SmartPrinter()
        self.args_manager = ArgumentsManager()
        self.github_client = None
        self.username = None
        self.stats = BackupStats()
        self.original_sigint = None

    def _signal_handler(self, signum, frame):
        print(f"\n\n⚠️ Received Ctrl+C - exiting immediately")
        self._show_footer()
        if self.original_sigint:
            signal.signal(signal.SIGINT, self.original_sigint)
        sys.exit(1)

    def _show_header(self):
        print()
        self.printer.show_header(text=Config.APP_NAME)
        print()

    def _show_footer(self):
        self.printer.show_footer(
            url=Config.APP_URL,
            copyright_=Config.APP_COPYRIGHT
        )

    def _check_network(self) -> bool:
        print("\n🌐 Network Check")

        if not NetworkChecker.check_internet():
            print("❌ No internet connection")
            return False

        print("✅ Internet connection OK")

        github_ok, message = NetworkChecker.check_github()
        if not github_ok:
            print(f"❌ GitHub check failed: {message}")
            return False

        print("✅ GitHub accessible")
        return True

    def _setup_app_directory(self) -> bool:
        print("\n📁 Application Setup")

        try:
            app_dir = ProjectPaths.get_app_dir()
            app_dir.mkdir(exist_ok=True, parents=True)
            print(f"   Application directory: {app_dir}")
            return True
        except Exception as e:
            print(f"❌ Failed to create app directory: {e}")
            return False

    def run(self):
        self.original_sigint = signal.getsignal(signal.SIGINT)
        signal.signal(signal.SIGINT, self._signal_handler)

        self._show_header()

        backup_repos = self.args_manager.print_args_info()
        args = self.args_manager.args

        if not backup_repos and not args.token:
            print("\n❌ Error: Specify at least one operation (-r for repos or -t for token)")
            self._show_footer()
            return

        if not self._setup_app_directory():
            self._show_footer()
            return

        if args.token:
            print("\n🔑 Token Update")
            users = ProjectPaths.get_all_users()
            if users:
                Config.delete_token(users[0])
                print(f"✅ Old token deleted for user: {users[0]}")

                print("\n🔐 GitHub Authentication")
                token = GitHubAuthManager.get_token_from_user()
                if token:
                    client = GitHubAPIClient(token, timeout=args.timeout)
                    if client.verify_token():
                        username = client.login
                        ProjectPaths.ensure_user_dir(username)
                        if Config.save_token(username, token):
                            print(f"✅ New token saved for user: {username}")
                        else:
                            print("❌ Failed to save new token")
                    else:
                        print("❌ New token is invalid")
                else:
                    print("❌ Token update cancelled")
            else:
                print("⚠️ No saved token found")
                print("\n🔐 GitHub Authentication")
                token = GitHubAuthManager.get_token_from_user()
                if token:
                    client = GitHubAPIClient(token, timeout=args.timeout)
                    if client.verify_token():
                        username = client.login
                        ProjectPaths.ensure_user_dir(username)
                        if Config.save_token(username, token):
                            print(f"✅ Token saved for user: {username}")
                        else:
                            print("❌ Failed to save token")
                    else:
                        print("❌ Token is invalid")
            self._show_footer()
            return

        if not self._check_network():
            self._show_footer()
            return

        self.github_client = GitHubAuthManager.authenticate(
            token=None,
            timeout=args.timeout
        )

        if not self.github_client:
            print("\n❌ Authentication failed")
            self._show_footer()
            return

        self.username = self.github_client.login

        print("\n🔍 Scanning repositories...")
        repos = self.github_client.get_all_repos()

        if not repos:
            print("\n⚠️ No repositories found")
            self._show_footer()
            return

        print(f"\n✅ Found {len(repos)} repositories total")

        self.save_user_info()

        if backup_repos:
            repo_manager = RepoManager(
                github_client=self.github_client,
                timeout=args.timeout,
                max_retries=5
            )

            self.stats = repo_manager.process_repositories(repos, all_branches=args.all_branches)

        report_gen = ReportGenerator(
            github_client=self.github_client,
            stats=self.stats
        )
        report_data = report_gen.generate()
        report_gen.save(report_data)

        if args.archive and backup_repos:
            archive_manager = ArchiveManager(
                username=self.username
            )
            archive_manager.create_archive()

        self._show_footer()

    def save_user_info(self):
        print("\n📄 Saving user information...")

        url = f"https://api.github.com/user"
        user_data = self.github_client._make_request(url)

        if user_data:
            user_info = {
                "login": user_data.get('login'),
                "name": user_data.get('name'),
                "email": user_data.get('email'),
                "bio": user_data.get('bio'),
                "public_repos": user_data.get('public_repos'),
                "private_repos": user_data.get('total_private_repos', 0),
                "followers": user_data.get('followers'),
                "following": user_data.get('following'),
                "created_at": user_data.get('created_at'),
                "updated_at": user_data.get('updated_at'),
                "last_backup": datetime.now().isoformat()
            }

            user_info_path = ProjectPaths.get_user_dir(self.username) / "user_info.json"
            with open(user_info_path, 'w', encoding='utf-8') as f:
                json.dump(user_info, f, indent=2)

            print(f"   ✅ User info saved: {user_info_path}")
