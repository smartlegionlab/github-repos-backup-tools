from typing import Dict, Any
from tools.steps.base import BaseStep


class FetchGistsStep(BaseStep):
    def __init__(self):
        super().__init__(
            name="Fetch Gists",
            description="Fetching user gists from GitHub"
        )

    def execute(self, context: Dict[str, Any]) -> bool:
        print(f"🔧 {self.description}...")

        args = context.get('args', {})
        github_client = context.get('github_client')

        if not github_client:
            print("❌ No GitHub client found in context")
            return False

        if not getattr(args, 'gists', False):
            print("⚠️ Gists backup not requested - skipping")
            return True

        timeout = getattr(args, 'timeout', 30)

        print("📝 Fetching gists...")
        github_client.fetch_gists(max_retries=3, timeout=timeout)

        gists_count = len(github_client.gists)
        if gists_count == 0:
            print("⚠️ No gists found")
        else:
            print(f"✅ Found {gists_count} gists")

        self.success = True
        return True
