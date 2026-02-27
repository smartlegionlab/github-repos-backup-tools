# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
# https://github.com/smartlegionlab/
# --------------------------------------------------------
import argparse


class ArgumentsManager:
    def __init__(self):
        self._parser = self._create_parser()
        self._args = None

    @property
    def args(self):
        if self._args is None:
            self._args = self._parser.parse_args()
        return self._args

    @property
    def parser(self):
        return self._parser

    @staticmethod
    def _create_parser() -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            description="GitHub Repositories Backup Tools - Clone all your repositories with ALL branches"
        )

        parser.add_argument(
            "-r",
            "--repos",
            action="store_true",
            help="Clone/update repositories"
        )
        parser.add_argument(
            "-t",
            "--token",
            action="store_true",
            help="Update GitHub token"
        )
        parser.add_argument(
            "--no-archive",
            action="store_false",
            dest="archive",
            default=True,
            help="Disable backup archive creation"
        )
        parser.add_argument(
            "--timeout",
            type=int,
            default=30,
            help="Timeout for git operations in seconds (default: 30)"
        )
        parser.add_argument(
            "--no-branches",
            action="store_true",
            help="Disable branch synchronization (faster, but only default branch)"
        )

        power_group = parser.add_mutually_exclusive_group()
        power_group.add_argument(
            "--shutdown",
            action="store_true",
            help="Shutdown after completion"
        )
        power_group.add_argument(
            "--reboot",
            action="store_true",
            help="Reboot after completion"
        )
        return parser

    def print_args_info(self):
        args = self.args

        print("\n🔧 Arguments Parsing:")
        print("Parsing command line arguments...")

        backup_items = []
        if args.repos:
            backup_items.append("Repositories")
        if args.archive:
            backup_items.append("Archive")

        print("\nParsed arguments:")
        print(f"   Backup: {', '.join(backup_items) if backup_items else 'None'}")
        print(f"   Timeout: {args.timeout}s")
        print(f"   Branches: {'✅ Yes' if not args.no_branches else '❌ No (fast mode)'}")

        if args.shutdown:
            print("   Shutdown: ✅ After completion")
        elif args.reboot:
            print("   Reboot: ✅ After completion")
        else:
            print("   Power: ❌ No action")

        return bool(backup_items)
