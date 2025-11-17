# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# (see LICENSE for details).
# Copyright © 2025, Alexander Suvorov
# All rights reserved.
# --------------------------------------------------------
# https://github.com/smartlegionlab/
# --------------------------------------------------------
import os
import signal
import sys

from core.args_manager import ArgumentsManager
from core.auth_manager import GithubAuthManager
from core.config import Config, ConfigPathManager
from core.directory_manager import DirectoryManager
from core.repos_manager import RepositoriesManager
from core.smart_printer import SmartPrinter
from core.token_manager import TokenManager


class AppManager:
    def __init__(self):
        self.printer = SmartPrinter()
        self.config = Config()
        self.token_manager = None
        self.github_client = None
        self.args_manager = None
        self.dir_manager = None
        self.repo_manager = None

    def _signal_handler(self, signum, frame):
        _ = signum, frame
        print(f"\n\n🛑 Received Ctrl+C - exiting immediately\n")
        self._show_footer()
        os._exit(1)

    def run(self):
        signal.signal(signal.SIGINT, self._signal_handler)
        self._show_header()
        args_manager_status = self._parse_args()

        if not args_manager_status:
            print('❌ Error! No arguments found...')
            self._exit()

        config_file = self._create_config()

        if not config_file:
            print('❌ Error creating configuration...')
            self._exit()

        print(f"\n📁 Configuration directory: {config_file}")

        self.token_manager = TokenManager(config_file)

        token = self._get_token()

        if not token:
            print('❌ Failed to get token')
            self._exit()

        print('\n✅ Token obtained successfully')

        if self.args_manager.args.token:
            self._update_token()

        timeout = self.args_manager.args.timeout or 30

        token_verify_success, github_client = self._token_verify(token, timeout, 3)

        if not all([token_verify_success, github_client.login]):
            print("❌ Failed to authenticate with GitHub")
            choice = input('\nWant to update your token? WARNING! Old token will be completely deleted! [y/n]: ')
            if choice == 'y':
                self.token_manager.delete_config()
                self.token_manager.get_token()
                print('\n✅ Token obtained successfully')
                print('🛑 Rebooting app...')
            else:
                print('\n🛑 Shutting down...')
            self._exit()

        print(f"✅ Authenticated as: {github_client.login}")

        self.github_client = github_client

        create_dirs_status = self._create_backup_dirs()

        if not create_dirs_status:
            print(f"❌ Failed to create backup directory")
            self._exit()

        print(f"📁 Main backup directory: {self.dir_manager.backup_path}")

        if self.args_manager.args.repos:
            print("   ✅ repositories/")

        if self.args_manager.args.gists:
            print("   ✅ gists/")

        if not self.args_manager.args.repos and not self.args_manager.args.gists:
            print("⚠️ No backup operations selected - no subdirectories created")

        if self.args_manager.args.repos:
            repo_manager_status = self._clone_repositories(
                self.github_client,
                self.dir_manager.repo_path
            )

            if not repo_manager_status:
                print(f"❌ Error cloning repositories!\n")


    def _clone_repositories(self, github_client, target_dir):
        print("\n🔄 Repositories Operations")
        print("Fetching and cloning/updating repositories...")
        self.repo_manager = RepositoriesManager(
            github_client=github_client,
            repos_target_dir=target_dir
        )
        return self.repo_manager.execute()

    def _create_backup_dirs(self):
        print("\n📁 Directory Setup: ")
        print("Creating backup directory structure...")
        self.dir_manager = DirectoryManager(
            github_login=self.github_client.login
        )
        status = self.dir_manager.run()
        return status


    @staticmethod
    def _token_verify(token, timeout, max_retries):
        print("\n🔑 GitHub Authentication: ")
        print("Authenticating with GitHub...")
        success, github_client = GithubAuthManager.token_verify(token, timeout, max_retries)
        return success, github_client

    def _update_token(self):
        print('\n🔑 Update GitHub token: ')
        print('WARNING! Old token will be completely deleted!\n')
        choice = input('Update token [y/n]: ')
        if choice == 'y':
            self.token_manager.delete_config()
            self.token_manager.get_token()
        self._exit()

    @staticmethod
    def _create_config():
        print('\n⚙️ Configuration Setup: ')
        print("Checking and setting up configuration directories")
        config_file = ConfigPathManager.ensure_config_exists()
        return config_file

    def _get_token(self):
        print('\n🔑 Getting GitHub token: ')
        token = self.token_manager.get_token()
        return token

    def _exit(self):
        self._show_footer()
        sys.exit(0)

    def _parse_args(self):
        print('\n🔧 Arguments Parsing: ')
        print('Parsing command line arguments...')
        self.args_manager = ArgumentsManager()
        args = self.args_manager.args

        if not any([args.repos, args.gists, args.token]):
            self.args_manager.parser.print_usage()
            print("\n❌ Error: Specify at least one backup operation (-r or -g or -t)")
            return False

        print("\n📋 Parsed arguments:")

        backup_items = []
        if args.repos: backup_items.append("📦 Repositories")
        if args.gists: backup_items.append("📝 Gists")
        if args.archive: backup_items.append("🗄 Archive")

        print(f"   Backup: {', '.join(backup_items)}")
        print(f"   Timeout: {args.timeout}s")
        print(f"   Verbose: {'✅ Enabled' if args.verbose else '❌ Disabled'}")

        if args.shutdown:
            print("   Shutdown: ✅ After completion")
        elif args.reboot:
            print("   Reboot: ✅ After completion")
        else:
            print("   Power: ❌ No action")
        return True

    def _show_header(self):
        self.printer.show_head(text=self.config.app_name)
        self.printer.print_center()
        print()

    def _show_footer(self):
        self.printer.print_center()
        self.printer.show_footer(
            url=self.config.app_url,
            copyright_=self.config.app_copyright
        )
