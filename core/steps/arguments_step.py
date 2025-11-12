# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# (see LICENSE for details).
# Copyright © 2025, Alexander Suvorov
# All rights reserved.
# --------------------------------------------------------
# https://github.com/smartlegionlab/
# --------------------------------------------------------
import argparse
from typing import Dict, Any
from core.steps.base import BaseStep


class ArgumentsStep(BaseStep):
    def __init__(self):
        super().__init__(
            name="🔧 Arguments Parsing",
            description="Parsing command line arguments"
        )

    def execute(self, context: Dict[str, Any]) -> bool:
        print(f"🔧 {self.description}...")

        parser = self._create_parser()

        try:
            args = parser.parse_args()
        except SystemExit:
            return False

        if not any([args.repos, args.gists]):
            parser.print_usage()
            print("\n❌ Error: Specify at least one backup operation (-r or -g)")
            return False

        context['args'] = args
        self._display_arguments(args)
        self.success = True
        return True

    def _create_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            description="GitHub Repositories Backup Tools"
        )

        parser.add_argument("-r", "--repos", action="store_true",
                          help="Clone/update repositories")
        parser.add_argument("-g", "--gists", action="store_true",
                          help="Clone/update gists")
        parser.add_argument("--archive", action="store_true",
                          help="Create backup archive")
        parser.add_argument("--timeout", type=int, default=30,
                          help="Timeout for git operations (default: 30)")
        parser.add_argument("--verbose", action="store_true",
                          help="Enable verbose output")

        power_group = parser.add_mutually_exclusive_group()
        power_group.add_argument("--shutdown", action="store_true",
                               help="Shutdown after completion")
        power_group.add_argument("--reboot", action="store_true",
                               help="Reboot after completion")

        return parser

    def _display_arguments(self, args):
        print("📋 Parsed arguments:")

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
