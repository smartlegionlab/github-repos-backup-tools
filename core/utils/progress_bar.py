# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# (see LICENSE for details).
# Copyright © 2025, Alexander Suvorov
# All rights reserved.
# --------------------------------------------------------
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

    @staticmethod
    def _progress_bar(current, total, failed, message=""):
        console_width = ProgressBar._get_console_width()
        percent = (current / total) * 100

        progress_info = f'{percent:.2f}% | {current}/{total} | Failed: {failed}'
        if message:
            progress_info += f' | {message}'

        min_bar_length = 10
        available_width = console_width - len(progress_info) - 3

        if available_width >= min_bar_length:
            bar_length = available_width
        else:
            bar_length = min_bar_length
            max_info_length = console_width - (bar_length + 3)
            if len(progress_info) > max_info_length:
                progress_info = progress_info[:max_info_length - 3] + '...'

        filled_length = int(bar_length * current // total)
        bar = '#' * filled_length + '-' * (bar_length - filled_length)

        line = f'\r[{bar}] {progress_info}'
        sys.stdout.write(line.ljust(console_width))
        sys.stdout.flush()

    def __init__(self):
        pass

    def update(self, current, total, failed, message=""):
        self._clear_line()
        self._progress_bar(current, total, failed, message)

    def finish(self, message='Progress completed!'):
        # self._clear_line()
        print(f"\n[ok] {message}\n")
