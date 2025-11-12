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

from core.steps.archive_step import ArchiveStep
from core.steps.configuration_step import ConfigurationStep
from core.steps.arguments_step import ArgumentsStep
from core.steps.authentication_step import AuthenticationStep
from core.steps.directory_setup_step import DirectorySetupStep
from core.steps.gists_step import GistsStep
from core.steps.repositories_step import RepositoriesStep
from core.steps.system_actions_step import SystemActionsStep
from core.steps.verification_step import VerificationStep
from core.steps.report_step import ReportStep
from core.tools.printers import SmartPrinter
from core.tools.config import Config


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
            RepositoriesStep(),
            GistsStep(),
            VerificationStep(),
            ReportStep(),
            ArchiveStep(),
            SystemActionsStep(),
        ]

    def run(self):
        signal.signal(signal.SIGINT, self._signal_handler)

        try:
            self._show_header()

            for step_number, step in enumerate(self.steps, 1):
                self._show_step_header(step_number, step)

                success = step.execute(self.context)
                if not success:
                    self._show_step_failure(step_number, step)
                    break

                self._show_step_success(step_number, step)

            self._show_footer()

        except KeyboardInterrupt:
            print("\n🛑 Interrupted by user - exiting immediately")
            sys.exit(1)
        except Exception as e:
            print(f"\n⚠️ Critical error: {e}")
            sys.exit(1)
        finally:
            print("\n👋 Backup process finished")

    def _signal_handler(self, signum, frame):
        print(f"\n🛑 Received Ctrl+C - exiting immediately")
        os._exit(1)

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
