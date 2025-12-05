# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# (see LICENSE for details).
# Copyright © 2025, Alexander Suvorov
# All rights reserved.
# --------------------------------------------------------
# https://github.com/smartlegionlab/
# --------------------------------------------------------
import argparse


class ArgumentsManager:
    def __init__(self):
        self._parser = self._create_parser()

    @property
    def args(self):
        return self._parser.parse_args()

    @property
    def parser(self):
        return self._parser

    @staticmethod
    def _create_parser() -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser(
            description="GitHub Repositories Backup Tools"
        )

        parser.add_argument(
            "-r",
            "--repos",
            action="store_true",
            help="Clone/update repositories"
        )
        parser.add_argument(
            "-g",
            "--gists",
            action="store_true",
            help="Clone/update gists"
        )
        parser.add_argument(
            "-t",
            "--token",
            action="store_true",
            help="Update token"
        )
        parser.add_argument(
            "--no-archive",
            action="store_false",
            dest="archive",
            default=True,
            help="Disable backup archive creation (archive is created by default)"
        )
        parser.add_argument(
            "--timeout",
            type=int,
            default=30,
            help="Timeout for git operations (default: 30)"
        )
        parser.add_argument(
            "--verbose",
            action="store_true",
            help="Enable verbose output"
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
