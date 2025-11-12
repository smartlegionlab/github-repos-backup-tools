from tools.steps.authentication_step import AuthenticationStep
from tools.steps.configuration_step import ConfigurationStep
from tools.steps.arguments_step import ArgumentsStep
from tools.printers import SmartPrinter
from tools.config import Config


class AppManager:
    def __init__(self):
        self.config = Config()
        self.printer = SmartPrinter()
        self.context = {}
        self.steps = [
            ArgumentsStep(),
            ConfigurationStep(),
            AuthenticationStep(),
        ]

    def run(self):
        try:
            self._show_header()

            for step_number, step in enumerate(self.steps, 1):
                self._show_step_header(step_number, step)

                success = step.execute(self.context)
                if not success:
                    self._show_step_failure(step_number, step)
                    return

                self._show_step_success(step_number, step)

            self._show_footer()

        except KeyboardInterrupt:
            print("\n🛑 Interrupted by user")
        except Exception as e:
            print(f"\n⚠️ Critical error: {e}")

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
