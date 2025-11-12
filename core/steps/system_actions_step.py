# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# (see LICENSE for details).
# Copyright © 2025, Alexander Suvorov
# All rights reserved.
# --------------------------------------------------------
# https://github.com/smartlegionlab/
# --------------------------------------------------------
import os
import platform
from typing import Dict, Any
from core.steps.base import BaseStep


class SystemActionsStep(BaseStep):
    def __init__(self):
        super().__init__(
            name="⚡ System Actions",
            description="Executing system actions (shutdown/reboot)"
        )

    def execute(self, context: Dict[str, Any]) -> bool:
        print(f"🔧 {self.description}...")

        args = context.get('args', {})

        if getattr(args, 'shutdown', False):
            return self._shutdown_system()
        elif getattr(args, 'reboot', False):
            return self._reboot_system()
        else:
            print("⚠️ No system actions requested - skipping")
            return True

    def _shutdown_system(self) -> bool:
        print("🔄 Shutting down system...")
        try:
            if platform.system() == "Windows":
                os.system("shutdown /s /t 60")
            else:
                os.system("shutdown -h +1")
            print("✅ Shutdown scheduled in 60 seconds")
            self.success = True
            return True
        except Exception as e:
            print(f"❌ Failed to schedule shutdown: {e}")
            return False

    def _reboot_system(self) -> bool:
        print("🔄 Rebooting system...")
        try:
            if platform.system() == "Windows":
                os.system("shutdown /r /t 60")
            else:
                os.system("shutdown -r +1")
            print("✅ Reboot scheduled in 60 seconds")
            self.success = True
            return True
        except Exception as e:
            print(f"❌ Failed to schedule reboot: {e}")
            return False
