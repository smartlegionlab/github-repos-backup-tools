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


class SystemActionManager:
    def __init__(self, shutdown_flag=False, reboot_flag=False):
        self.shutdown_flag = shutdown_flag
        self.reboot_flag = reboot_flag

    def execute(self):
        if self.shutdown_flag:
            return self._shutdown_system()
        elif self.reboot_flag:
            return self._reboot_system()
        else:
            print("[!] No system actions requested - skipping")
            return True

    def _shutdown_system(self) -> bool:
        print("[~] Shutting down system...")
        try:
            if platform.system() == "Windows":
                os.system("shutdown /s /t 60")
            else:
                os.system("shutdown -h +1")
            print("[ok] Shutdown scheduled in 60 seconds")
            self.success = True
            return True
        except Exception as e:
            print(f"[err] Failed to schedule shutdown: {e}")
            return False

    def _reboot_system(self) -> bool:
        print("[~] Rebooting system...")
        try:
            if platform.system() == "Windows":
                os.system("shutdown /r /t 60")
            else:
                os.system("shutdown -r +1")
            print("[ok] Reboot scheduled in 60 seconds")
            self.success = True
            return True
        except Exception as e:
            print(f"[err] Failed to schedule reboot: {e}")
            return False
