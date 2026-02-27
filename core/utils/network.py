# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
# https://github.com/smartlegionlab/
# --------------------------------------------------------
import socket
import urllib.request
import urllib.error
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
            req = urllib.request.Request("https://api.github.com")
            req.add_header('User-Agent', 'GitHub-Backup-Tools/2.0')

            with urllib.request.urlopen(req, timeout=timeout) as response:
                if response.status == 200:
                    return True, "GitHub API is accessible"
                else:
                    return False, f"GitHub returned status {response.status}"

        except urllib.error.URLError as e:
            return False, f"Cannot connect to GitHub: {e.reason}"
        except TimeoutError:
            return False, "Connection timeout"
        except Exception as e:
            return False, str(e)
