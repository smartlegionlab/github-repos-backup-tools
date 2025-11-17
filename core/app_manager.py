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

from core.args_parser import ArgumentsParser
from core.auth_manager import GithubAuthManager
from core.config import Config, ConfigPathManager
from core.smart_printer import SmartPrinter
from core.token_manager import TokenManager


class AppManager:
    def __init__(self):
        self.printer = SmartPrinter()
        self.config = Config()
        self.token_manager = None
        self.github_client = None

    def _signal_handler(self, signum, frame):
        _ = signum, frame
        print(f"\n\n🛑 Received Ctrl+C - exiting immediately\n")
        self._show_footer()
        os._exit(1)

    def run(self):
        signal.signal(signal.SIGINT, self._signal_handler)
        self._show_header()
        args = self._parse_args()

        if not args:
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

        if args.token:
            self._update_token()

        timeout = args.timeout or 30

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

    @staticmethod
    def _parse_args():
        print('\n🔧 Arguments Parsing: ')
        print('Parsing command line arguments...')
        parser = ArgumentsParser()
        args = parser.args
        if not any([args.repos, args.gists, args.token]):
            parser.parser.print_usage()
            print("\n❌ Error: Specify at least one backup operation (-r or -g)")
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
        return args

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
