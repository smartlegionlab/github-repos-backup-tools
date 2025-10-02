# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# (see LICENSE for details).
# Copyright © 2025, Alexander Suvorov
# All rights reserved.
# --------------------------------------------------------
# https://github.com/smartlegionlab/
# --------------------------------------------------------
import os
import shutil
import subprocess
import argparse
import sys
from typing import Dict
import platform
from datetime import datetime, timezone

from utils.backup_reporter import BackupReporter
from utils.archive_creator import ArchiveCreator
from utils.config import Config
from utils.github_tools import GitHubDataMaster
from utils.parsers import ConfigParser
from utils.printers import SmartPrinter
from utils.progress_bar import ProgressBar


class AppManager:
    def __init__(
            self,
            config=Config(),
            printer=SmartPrinter(),
            config_parser=ConfigParser(),
            github_data_master=GitHubDataMaster(),
            timeout=30
    ):
        self.config = config
        self.printer = printer
        self.config_parser = config_parser
        self.github_data_master = github_data_master
        self.shutdown_flag = False
        self.verbose = False
        self.timeout = timeout

    def graceful_shutdown(self):
        if self.shutdown_flag:
            return
        self.shutdown_flag = True
        print("\n🛑 Shutting down gracefully...")
        self.stop()
        sys.exit(0)

    def _get_local_commit_date(self, item_path: str) -> datetime:
        try:
            git_dir = os.path.join(item_path, '.git')
            if not os.path.exists(git_dir):
                return datetime.min

            check_result = subprocess.run(
                ['git', '-C', item_path, 'rev-parse', '--verify', 'HEAD'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=5
            )

            if check_result.returncode != 0:
                return datetime.min

            result = subprocess.run(
                ['git', '-C', item_path, 'show', '-s', '--format=%ci', 'HEAD'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=5
            )

            if result.returncode == 0 and result.stdout.strip():
                date_line = result.stdout.strip().split('\n')[0]
                if date_line:
                    try:
                        date_str_clean = date_line.replace(' +', '+').replace(' -', '-')
                        return datetime.fromisoformat(date_str_clean)
                    except ValueError:
                        pass

            return datetime.min

        except Exception:
            return datetime.min

    def _needs_update(self, item_path: str, github_pushed_at: str) -> bool:
        try:
            local_date = self._get_local_commit_date(item_path)
            github_date = datetime.fromisoformat(github_pushed_at.replace('Z', '+00:00'))

            if local_date.tzinfo is not None:
                local_date_utc = local_date.astimezone(timezone.utc).replace(tzinfo=None)
            else:
                local_date_utc = local_date

            github_date_utc = github_date.replace(tzinfo=None)

            time_diff = github_date_utc - local_date_utc
            needs_update = time_diff.total_seconds() > 30

            if self.verbose:
                print(f"🔍 Date comparison:")
                print(f"   GitHub (UTC): {github_date_utc}")
                print(f"   Local (UTC):  {local_date_utc}")
                print(f"   Difference:   {time_diff.total_seconds()} sec")
                print(f"   Needs update: {needs_update} (threshold: 30 sec)")

            return needs_update

        except Exception as e:
            if self.verbose:
                print(f"⚠️ Date check error, will update: {str(e)}")
            return True

    @staticmethod
    def _parse_arguments():
        parser = argparse.ArgumentParser(description="GitHub Repos Backup Tools")
        parser.add_argument("-r", action="store_true", help="Clone repositories")
        parser.add_argument("-g", action="store_true", help="Clone gists")
        parser.add_argument("--archive", action="store_true", help="Create archive")
        parser.add_argument("--timeout", type=int, default=30,
                            help="Timeout for git operations in seconds (default: 30)", )
        mutex_group = parser.add_mutually_exclusive_group()
        mutex_group.add_argument("--shutdown", action="store_true", help="Shutdown after completion")
        mutex_group.add_argument("--reboot", action="store_true", help="Reboot after completion")
        parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
        return parser.parse_args()

    @staticmethod
    def _create_clone_directory(login) -> str:
        home_directory = os.path.expanduser('~')
        clone_path = os.path.join(home_directory, f'{login}_github_backup')
        os.makedirs(clone_path, exist_ok=True)
        return clone_path

    @staticmethod
    def shutdown():
        print()
        if platform.system() == "Windows":
            os.system("shutdown /s /t 60")
        else:
            os.system("shutdown -h +1")
        print()

    @staticmethod
    def reboot():
        print()
        if platform.system() == "Windows":
            os.system("shutdown /r /t 60")
        else:
            os.system("shutdown -r +1")
        print()

    @staticmethod
    def get_yes_no(arg):
        return '✅' if arg else '⚠️'

    @staticmethod
    def create_item_path(target_dir: str, item_name: str) -> str:
        item_path = os.path.normpath(os.path.join(target_dir, os.path.basename(item_name)))

        if not item_path.startswith(os.path.abspath(target_dir) + os.sep):
            raise ValueError(f"Potential path traversal attack! Blocked: {item_path}")

        return item_path

    def _git_clone(self, url: str, item_path: str) -> bool:
        try:
            result = subprocess.run(
                ['git', 'clone', url, item_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=self.timeout
            )
            if result.returncode == 0:
                if self.verbose:
                    print(f"✅ Repository cloned successfully: \n{item_path}")
                return True
            else:
                if self.verbose:
                    print(f"⚠️ Failed to clone repository: \n{item_path}")
                    print(result.stderr)
                return False
        except subprocess.TimeoutExpired:
            if self.verbose:
                print(f"⚠️ Clone operation timed out: \n{item_path}")
            return False
        except Exception as e:
            if self.verbose:
                print(f"⚠️ An unexpected error occurred while cloning {item_path}: {str(e)}")
            return False

    def _git_pull(self, item_path: str) -> bool:
        try:
            result = subprocess.run(
                ['git', '-C', item_path, 'pull', 'origin', 'master'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=self.timeout
            )
            if result.returncode == 0:
                if self.verbose:
                    print(f"✅ Repository updated successfully: \n{item_path}")
                return True
            else:
                if self.verbose:
                    print(f"⚠️ Failed to update repository: \n{item_path}")
                    print(result.stderr)
                return False
        except subprocess.TimeoutExpired:
            if self.verbose:
                print(f"⚠️ Pull operation timed out: \n{item_path}")
            return False
        except Exception as e:
            if self.verbose:
                print(f"⚠️ An unexpected error occurred while updating {item_path}: {str(e)}")
            return False

    def start(self):
        self.printer.show_head(text=self.config.name)
        self.printer.print_center()
        print()
        token = self.config_parser.get_token()
        print(f'Getting a token from a .config.ini file: {self.get_yes_no(token)}\n')

        if not token:
            print("⚠️ ERROR! Please provide GitHub token in the config file.")
            return

        print('Parsing arguments:\n')
        args = self._parse_arguments()
        self.timeout = args.timeout
        print(f'Git operations timeout: {self.timeout} seconds ✅')
        clone_repos = args.r
        clone_gists = args.g
        make_archive = args.archive
        exec_shutdown = args.shutdown
        exec_reboot = args.reboot
        self.verbose = args.verbose

        print(f'Clone repositories: {self.get_yes_no(clone_repos)}')
        print(f'Clone gists: {self.get_yes_no(clone_gists)}')
        print(f'Make archive: {self.get_yes_no(make_archive)}')
        print(f'Shutdown: {self.get_yes_no(exec_shutdown)}')
        print(f'Reboot: {self.get_yes_no(exec_reboot)}')
        print(f'Verbose: {self.get_yes_no(self.verbose)}\n')

        self.github_data_master.token = token
        print(f'Checking the token for validity:')
        is_token_valid = self.github_data_master.is_token_valid()
        print(f'Token is valid: {self.get_yes_no(is_token_valid)}\n')

        if not is_token_valid:
            print('⚠️ Error! Token is not valid.')
            return

        print('Getting user login:')
        self.github_data_master.fetch_user_data()
        login = self.github_data_master.login

        if not login:
            print('⚠️ Login failed.')
            return

        print(f'✅ Login: {login}\n')

        print('Forming a path to the directory:')
        path = self._create_clone_directory(login)
        print(f'✅ Path: {path}\n')

        repos_failed = {}
        gists_failed = {}

        if clone_repos:
            repos_target_dir = os.path.join(path, "repositories")
            repos_failed = self.clone_items(repos_target_dir, self.github_data_master.fetch_repositories,
                                            "repositories")

        if clone_gists:
            gists_target_dir = os.path.join(path, "gists")
            gists_failed = self.clone_items(gists_target_dir, self.github_data_master.fetch_gists, "gists")

        if make_archive:
            self._create_archive(login)

        try:
            repos_data_for_report = {}
            if hasattr(self.github_data_master, "repositories"):
                for name, data in self.github_data_master.repositories.items():
                    if isinstance(data, dict):
                        repos_data_for_report[name] = data['ssh_url']
                    else:
                        repos_data_for_report[name] = data

            gists_data_for_report = self.github_data_master.gists

            report = BackupReporter.generate(
                clone_repos=clone_repos,
                clone_gists=clone_gists,
                make_archive=make_archive,
                repos_data=repos_data_for_report,
                gists_data=gists_data_for_report,
                failed_repos=repos_failed,
                failed_gists=gists_failed,
                backup_path=path
            )
            self.printer.print_center(text=' REPORT: ')
            print(report)
        except Exception as e:
            print(f'Report generation failed: {str(e)}')

        if exec_shutdown:
            self.shutdown()
        elif exec_reboot:
            self.reboot()

    def clone_items(self, target_dir: str, fetch_method, item_type: str) -> Dict[str, bool]:
        print()
        self.printer.print_center()
        self.printer.print_center(text=f'Cloning {item_type}: ')
        self.printer.print_center()
        print()
        os.makedirs(target_dir, exist_ok=True)
        print(f'Target directory: {target_dir}\n')
        print(f'Getting {item_type}:\n')
        fetch_method()
        items = getattr(self.github_data_master, item_type)
        count = len(items)

        if not count:
            self.printer.print_framed(f'⚠️ No {item_type} found. \n')
            return {}
        else:
            self.printer.print_framed(f'✅ Found {count} {item_type} ')
        print()
        failed_dict = {}
        failed_count = 0
        progress_bar = ProgressBar()

        for index, (name, item_data) in enumerate(items.items(), start=1):
            if not self.verbose:
                progress_bar.update(index, count, failed_count, f"Processing: {name}")
            else:
                self.printer.print_framed(f'{index}/{count}/{failed_count}: Processing: {name}')

            if item_type == "repositories":
                if isinstance(item_data, dict):
                    url = item_data['ssh_url']
                    pushed_at = item_data.get('pushed_at')
                else:
                    url = item_data
                    pushed_at = None
            else:
                url = item_data
                pushed_at = None

            item_path = self.create_item_path(target_dir, name)

            if os.path.exists(item_path):
                if pushed_at:
                    needs_update = self._needs_update(item_path, pushed_at)

                    if not needs_update:
                        success = True
                        if self.verbose:
                            print(f"✅ Already up to date: {name}")
                    else:
                        success = self._git_pull(item_path)
                        if not success:
                            if self.verbose:
                                print(f"⚠️ Pull failed. Removing and re-cloning: \n{item_path}")
                            shutil.rmtree(item_path)
                            success = self._git_clone(url, item_path)
                else:
                    success = self._git_pull(item_path)
                    if not success:
                        if self.verbose:
                            print(f"⚠️ Pull failed. Removing and re-cloning: \n{item_path}")
                        shutil.rmtree(item_path)
                        success = self._git_clone(url, item_path)
            else:
                success = self._git_clone(url, item_path)

            if not success:
                if self.verbose:
                    print(f"⚠️ Removing incomplete {item_type}: \n{item_path}")
                if os.path.exists(item_path):
                    shutil.rmtree(item_path)
                failed_dict[name] = url
                failed_count += 1

        if not failed_dict:
            if not self.verbose:
                progress_bar.finish(message=f'Cloning/updating {item_type} completed successfully!!!')
            return failed_dict

        while failed_dict:
            if self.verbose:
                self.printer.print_center()
                print()
                self.printer.print_framed(f"Retrying failed {item_type}: {len(failed_dict)} remaining")
                print()
                self.printer.print_center()

            current_failed = failed_dict.copy()
            failed_dict.clear()

            for index, (name, url) in enumerate(current_failed.items(), start=1):
                if not self.verbose:
                    progress_bar.update(index, len(current_failed), failed_count, f"Retrying: {name}")
                else:
                    self.printer.print_framed(f'{index}/{len(current_failed)}/{failed_count}: Retrying: {name}')

                item_path = self.create_item_path(target_dir, name)

                if os.path.exists(item_path):
                    success = self._git_pull(item_path)
                    if not success:
                        if self.verbose:
                            print(f"⚠️ Pull failed. Removing and re-cloning: \n{item_path}")
                        shutil.rmtree(item_path)
                        success = self._git_clone(url, item_path)
                else:
                    success = self._git_clone(url, item_path)

                if not success:
                    if self.verbose:
                        print(f"⚠️ Removing incomplete {item_type}: \n{item_path}")
                    if os.path.exists(item_path):
                        shutil.rmtree(item_path)
                    failed_dict[name] = url
                else:
                    failed_count -= 1

        if not self.verbose:
            progress_bar.finish(message=f'Cloning/updating {item_type} completed successfully!!!')
        return failed_dict

    def _create_archive(self, login):
        home_directory = os.path.expanduser('~')
        clone_path = os.path.join(home_directory, f'{login}_github_backup')
        if os.path.exists(clone_path):
            archive_creator = ArchiveCreator(clone_path)
            archive_creator.create_archive()
        else:
            self.printer.print_framed("⚠️ Clone path not found ")

    def stop(self, shutdown=False):
        self.printer.print_center()
        self.printer.show_footer(url=self.config.url, copyright_=self.config.info)
        if shutdown:
            self.shutdown()

    def run(self):
        try:
            self.start()
            self.stop()
        except KeyboardInterrupt:
            print("\n🛑 Detected Ctrl+C. Shutting down...")
            self.graceful_shutdown()
        except Exception as e:
            print(f"⚠️ An unexpected error occurred: {e}")
            self.graceful_shutdown()
        finally:
            print("\n✅ Application has been terminated. You can now close the console.")
            sys.exit(0)
