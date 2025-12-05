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

from core.managers.archive_manager import ArchiveManager
from core.managers.args_manager import ArgumentsManager
from core.managers.auth_manager import GithubAuthManager
from core.managers.config_manager import Config, ConfigPathManager
from core.managers.directory_manager import DirectoryManager
from core.managers.gists_manager import GistsManager
from core.managers.report_manager import ReportManager
from core.managers.repos_manager import RepositoriesManager
from core.utils.smart_printer import SmartPrinter
from core.managers.system_action_manager import SystemActionManager
from core.managers.token_manager import TokenManager
from core.managers.verify_manager import VerifyManager


class AppManager:
    def __init__(self):
        self.printer = SmartPrinter()
        self.config = Config()
        self.token_manager = None
        self.github_client = None
        self.args_manager = None
        self.dir_manager = None
        self.repo_manager = None
        self.gists_manager = None
        self.verify_manager = None
        self.report_manager = None
        self.archive_manager = None
        self.system_action_manager = None

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

        github_login = github_client.login if github_client else False

        if not all([token_verify_success, github_login]):
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

        if self.args_manager.args.gists:
            gists_manager_status = self._clone_gists(
                self.github_client,
                self.dir_manager.gists_path
            )

            if not gists_manager_status:
                print(f"❌ Error cloning gists!\n")

        verify_status = self._run_verification()

        if not verify_status:
            print('❌ Error! Verification failed!')

        report_status = self._get_report()

        if not report_status:
            print('❌ Generating backup report error!')

        if self.args_manager.args.archive:
            archive_status = self._create_archive()
            if not archive_status:
                print("❌ Archive creation error!")

        if self.args_manager.args.shutdown or self.args_manager.args.reboot:
            system_action_status = self._start_system_actions()
            if not system_action_status:
                print("❌ System action error!")

        self._show_footer()

    def _start_system_actions(self):
        print("\n⚡ System Actions: ")
        print("Executing system actions (shutdown/reboot)")
        self.system_action_manager = SystemActionManager(
            shutdown_flag=self.args_manager.args.shutdown,
            reboot_flag=self.args_manager.args.reboot
        )
        return self.system_action_manager.execute()

    def _create_archive(self):
        print("\n🗄️ Archive Creation: ")
        self.archive_manager = ArchiveManager(
            backup_path=self.dir_manager.backup_path,
            github_login=self.github_client.login
        )
        return self.archive_manager.execute()

    def _get_report(self):
        print("\n📊 Report: ")
        print("Generating backup report...")
        self.report_manager = ReportManager(
            github_client=self.github_client,
            backup_path=self.dir_manager.backup_path,
            failed_repos=self.repo_manager.failed_repos if self.repo_manager else {},
            failed_gists=self.gists_manager.failed_gists if self.gists_manager else {},
            repo_flag=self.args_manager.args.repos,
            gists_flag=self.args_manager.args.gists,
        )
        return self.report_manager.execute()


    def _run_verification(self):
        print('\n✅ Verification: ')
        print('Verifying that all repositories and gists are properly cloned/updated...')
        self.verify_manager = VerifyManager(
            github_client=self.github_client,
            backup_path=self.dir_manager.backup_path,
            failed_repos=self.repo_manager.failed_repos if self.repo_manager else {},
            failed_gists=self.gists_manager.failed_gists if self.gists_manager else {},
            repo_flag=self.args_manager.args.repos,
            gists_flag=self.args_manager.args.gists,
        )
        return self.verify_manager.execute()


    def _clone_repositories(self, github_client, target_dir):
        print("\n🔄 Repositories Operations: ")
        print("Fetching and cloning/updating repositories...")
        self.repo_manager = RepositoriesManager(
            github_client=github_client,
            repos_target_dir=target_dir,
            verbose=self.args_manager.args.verbose
        )
        return self.repo_manager.execute()

    def _clone_gists(self, github_client, target_dir):
        print("\n🔄 Gists Operations: ")
        print("Fetching and cloning/updating gists...")
        self.gists_manager = GistsManager(
            github_client=github_client,
            gists_target_dir=target_dir,
            verbose=self.args_manager.args.verbose
        )
        return self.gists_manager.execute()

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
