# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# (see LICENSE for details).
# Copyright © 2025, Alexander Suvorov
# All rights reserved.
# --------------------------------------------------------
# https://github.com/smartlegionlab/
# --------------------------------------------------------
"""A professional, modular solution for automatically cloning and backing up GitHub repositories and GIST files."""
from core import AppManager


def main():
    app = AppManager()
    app.run()


if __name__ == '__main__':
    main()
