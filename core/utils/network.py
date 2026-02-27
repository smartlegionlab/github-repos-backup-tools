# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
# https://github.com/smartlegionlab/
# --------------------------------------------------------
import socket
import requests
from typing import Tuple


class NetworkChecker:

    @staticmethod
    def check_internet(host: str = "8.8.8.8", port: int = 53, timeout: int = 3) -> bool:
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            return True
        except Exception:
            return False

    @staticmethod
    def check_github(timeout: int = 5) -> Tuple[bool, str]:
        try:
            response = requests.get("https://api.github.com", timeout=timeout)
            if response.status_code == 200:
                return True, "GitHub API is accessible"
            else:
                return False, f"GitHub returned status {response.status_code}"
        except requests.exceptions.Timeout:
            return False, "Connection timeout"
        except requests.exceptions.ConnectionError:
            return False, "Cannot connect to GitHub"
        except Exception as e:
            return False, str(e)
