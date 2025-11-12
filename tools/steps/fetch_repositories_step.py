from typing import Dict, Any
from tools.steps.base import BaseStep


class FetchRepositoriesStep(BaseStep):
    def __init__(self):
        super().__init__(
            name="Fetch Repositories",
            description="Fetching user repositories from GitHub"
        )

    def execute(self, context: Dict[str, Any]) -> bool:
        print(f"🔧 {self.description}...")

        args = context.get('args', {})
        github_client = context.get('github_client')

        if not github_client:
            print("❌ No GitHub client found in context")
            return False

        if not getattr(args, 'repos', False):
            print("⚠️ Repository backup not requested - skipping")
            return True

        timeout = getattr(args, 'timeout', 30)

        print("📦 Fetching repositories...")
        github_client.fetch_repositories(max_retries=3, timeout=timeout)

        repos_count = len(github_client.repositories)
        if repos_count == 0:
            print("⚠️ No repositories found")
        else:
            print(f"✅ Found {repos_count} repositories")

        self.success = True
        return True
