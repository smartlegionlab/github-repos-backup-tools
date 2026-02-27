# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
# https://github.com/smartlegionlab/
# --------------------------------------------------------
import sys
import shutil


class ProgressBar:
    @staticmethod
    def _clear_line():
        sys.stdout.write('\r\033[K')
        sys.stdout.flush()

    @staticmethod
    def _get_console_width():
        return shutil.get_terminal_size().columns

    def update(self, current: int, total: int, failed: int = 0, message: str = ""):
        self._clear_line()

        console_width = self._get_console_width()
        percent = (current / total) * 100 if total > 0 else 0

        progress_info = f' {percent:.1f}% | {current}/{total}/{failed} | '

        if message:
            max_msg_len = console_width - len(progress_info) - 20
            if len(message) > max_msg_len:
                message = message[:max_msg_len - 3] + '...'
            progress_info += message

        bar_length = console_width - len(progress_info) - 5
        if bar_length > 10:
            filled = int(bar_length * current // total) if total > 0 else 0
            bar = '█' * filled + '░' * (bar_length - filled)
            line = f'\r[{bar}] {progress_info}'
        else:
            line = f'\r{progress_info}'

        sys.stdout.write(line)
        sys.stdout.flush()

    def finish(self, message: str = "Complete!"):
        self._clear_line()
        print(f"\n✅ {message}")
