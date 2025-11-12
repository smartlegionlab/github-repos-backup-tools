from tools.steps.configuration_step import ConfigurationStep
from tools.steps.arguments_step import ArgumentsStep
from tools.steps.authentication_step import AuthenticationStep
from tools.steps.directory_setup_step import DirectorySetupStep
from tools.steps.fetch_repositories_step import FetchRepositoriesStep
from tools.steps.fetch_gists_step import FetchGistsStep
from tools.steps.git_operations_step import GitOperationsStep
from tools.steps.verification_step import VerificationStep
from tools.steps.report_step import ReportStep
from tools.printers import SmartPrinter
from tools.config import Config
import signal


class AppManager:
    def __init__(self):
        self.config = Config()
        self.printer = SmartPrinter()
        self.context = {}
        self.steps = [
            ArgumentsStep(),
            ConfigurationStep(),
            AuthenticationStep(),
            DirectorySetupStep(),
            FetchRepositoriesStep(),
            FetchGistsStep(),
            GitOperationsStep(),
            VerificationStep(),
            ReportStep(),
        ]
        self.shutdown_flag = False

    def run(self):
        signal.signal(signal.SIGINT, self._signal_handler)

        try:
            self._show_header()

            for step_number, step in enumerate(self.steps, 1):
                if self.shutdown_flag:
                    print("\n🛑 Shutdown requested - stopping gracefully")
                    break

                self._show_step_header(step_number, step)

                success = step.execute(self.context)
                if not success:
                    self._show_step_failure(step_number, step)
                    break

                self._show_step_success(step_number, step)

            self._show_footer()

        except KeyboardInterrupt:
            print("\n🛑 Interrupted by user")
        except Exception as e:
            print(f"\n⚠️ Critical error: {e}")
        finally:
            print("\n👋 Backup process finished")

    def _signal_handler(self, signum, frame):
        print(f"\n🛑 Received interrupt signal (Ctrl+C) - shutting down gracefully...")
        self.shutdown_flag = True

    def _show_step_header(self, step_number: int, step):
        print(f"\n{'=' * 50}")
        print(f"STEP {step_number}: {step.name}")
        print(f"{'=' * 50}")

    def _show_step_success(self, step_number: int, step):
        print(f"✅ Step {step_number} completed: {step.name}")

    def _show_step_failure(self, step_number: int, step):
        print(f"❌ Step {step_number} failed: {step.name}")

    def _show_header(self):
        self.printer.show_head(text=self.config.name)
        self.printer.print_center()
        print()

    def _show_footer(self):
        self.printer.print_center()
        self.printer.show_footer(url=self.config.url, copyright_=self.config.info)

    def add_step(self, step):
        self.steps.append(step)

    def insert_step(self, index: int, step):
        self.steps.insert(index, step)
