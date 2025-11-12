from typing import Dict, Any
from tools.steps.base import BaseStep
from tools.github_tools import GitHubDataMaster


class AuthenticationStep(BaseStep):
    def __init__(self):
        super().__init__(
            name="GitHub Authentication",
            description="Authenticating with GitHub and fetching user data"
        )

    def execute(self, context: Dict[str, Any]) -> bool:
        print(f"🔧 {self.description}...")

        github_token = context.get('github_token')
        if not github_token:
            print("❌ No GitHub token found in context")
            return False

        args = context.get('args', {})
        fetch_repos = getattr(args, 'repos', False)
        fetch_gists = getattr(args, 'gists', False)
        timeout = getattr(args, 'timeout', 30)

        github_client = GitHubDataMaster(github_token)

        print("🔑 Validating token and fetching user data...")
        success = github_client.fetch_user_data(max_retries=3, timeout=timeout)

        if not success or not github_client.login:
            print("❌ Failed to authenticate with GitHub")
            return False

        print(f"✅ Authenticated as: {github_client.login}")

        if fetch_repos:
            print("📦 Fetching repositories...")
            github_client.fetch_repositories(max_retries=3, timeout=timeout)
            repos_count = len(github_client.repositories)
            print(f"✅ Found {repos_count} repositories")

        if fetch_gists:
            print("📝 Fetching gists...")
            github_client.fetch_gists(max_retries=3, timeout=timeout)
            gists_count = len(github_client.gists)
            print(f"✅ Found {gists_count} gists")

        context['github_client'] = github_client
        context['github_login'] = github_client.login

        self.success = True
        return True
