# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# (see LICENSE for details).
# Copyright © 2025, Alexander Suvorov
# All rights reserved.
# --------------------------------------------------------
# https://github.com/smartlegionlab/
# --------------------------------------------------------
from core.utils.github_tools import GitHubDataMaster


class GithubAuthManager:

    @classmethod
    def token_verify(cls, token, timeout, max_retries=3):
        github_client = GitHubDataMaster(token)
        success = github_client.fetch_user_data(max_retries=max_retries, timeout=timeout)
        if not success or not github_client.login:
            return False, None
        return True, github_client
