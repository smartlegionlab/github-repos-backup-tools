# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# (see LICENSE for details).
# Copyright © 2025, Alexander Suvorov
# All rights reserved.
# --------------------------------------------------------
# https://github.com/smartlegionlab/
# --------------------------------------------------------
from typing import Dict, Any
from core.steps.base import BaseStep
from core.tools.github_tools import GitHubDataMaster


class AuthenticationStep(BaseStep):
    def __init__(self):
        super().__init__(
            name="🔑 GitHub Authentication",
            description="Authenticating with GitHub"
        )

    def execute(self, context: Dict[str, Any]) -> bool:
        print(f"🔧 {self.description}...")

        github_token = context.get('github_token')
        if not github_token:
            print("❌ No GitHub token found in context")
            return False

        timeout = getattr(context.get('args', {}), 'timeout', 30)

        github_client = GitHubDataMaster(github_token)

        print("🔑 Validating GitHub token...")

        success = github_client.fetch_user_data(max_retries=3, timeout=timeout)

        if not success or not github_client.login:
            print("❌ Failed to authenticate with GitHub")
            return False

        print(f"✅ Authenticated as: {github_client.login}")

        context['github_client'] = github_client
        context['github_login'] = github_client.login

        self.success = True
        return True
