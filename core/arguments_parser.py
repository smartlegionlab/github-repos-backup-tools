import argparse


class ArgumentsParser:
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
            "--archive",
            action="store_true",
            help="Create backup archive"
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
