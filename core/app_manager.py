import sys

from core.arguments_parser import ArgumentsParser
from core.config import Config, ConfigPathManager
from core.smart_printer import SmartPrinter


class AppManager:
    def __init__(self):
        self.printer = SmartPrinter()
        self.config = Config()

    def run(self):
        self._show_header()
        args = self._parse_args()

        if not args:
            print('❌ Error! No arguments found...')
            self._exit()

        config_path = self._get_config_path()

        if not config_path:
            print('❌ Error creating configuration directory...')
            self._exit()

    def _exit(self):
        self._show_footer()
        sys.exit(0)

    def _get_config_path(self):
        print('\n⚙️ Configuration Setup: ')
        print("Checking and setting up configuration directories")
        try:
            config_path_man = self.config_path_man = ConfigPathManager()
            config_path = config_path_man.config_dir
            print(f"\n📁 Configuration directory: {config_path}")
            return config_path
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def _parse_args():
        print('\n🔧 Arguments Parsing: ')
        print('Parsing command line arguments...')
        parser = ArgumentsParser()
        args = parser.args
        if not any([args.repos, args.gists]):
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
