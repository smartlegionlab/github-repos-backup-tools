# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# (see LICENSE for details).
# Copyright © 2025, Alexander Suvorov
# All rights reserved.
# --------------------------------------------------------
# https://github.com/smartlegionlab/
# --------------------------------------------------------
from typing import Dict, Any
from tools.steps.base import BaseStep


class ReportStep(BaseStep):
    def __init__(self):
        super().__init__(
            name="Report",
            description="Generating backup report"
        )

    def execute(self, context: Dict[str, Any]) -> bool:
        print(f"🔧 {self.description}...")

        args = context.get('args', {})
        github_client = context.get('github_client')
        backup_path = context.get('backup_path')
        failed_repos = context.get('failed_repos', {})
        failed_gists = context.get('failed_gists', {})

        if not backup_path:
            print("❌ Missing backup path in context")
            return False

        print("\n" + "=" * 60)
        print("📊 BACKUP REPORT")
        print("=" * 60)

        total_success = True

        if getattr(args, 'repos', False) and github_client and github_client.repositories:
            total_repos = len(github_client.repositories)
            successful_repos = total_repos - len(failed_repos)

            print(f"\n📦 REPOSITORIES:")
            print(f"   Total: {total_repos}")
            print(f"   ✅ Successful: {successful_repos}")
            print(f"   ❌ Failed: {len(failed_repos)}")

            if failed_repos:
                print(f"   Failed items: {', '.join(list(failed_repos.keys())[:3])}" +
                      (f" ... and {len(failed_repos) - 3} more" if len(failed_repos) > 3 else ""))
                total_success = False
            else:
                print("   🎉 All repositories processed successfully!")

        if getattr(args, 'gists', False) and github_client and github_client.gists:
            total_gists = len(github_client.gists)
            successful_gists = total_gists - len(failed_gists)

            print(f"\n📝 GISTS:")
            print(f"   Total: {total_gists}")
            print(f"   ✅ Successful: {successful_gists}")
            print(f"   ❌ Failed: {len(failed_gists)}")

            if failed_gists:
                print(f"   Failed items: {', '.join(list(failed_gists.keys())[:3])}" +
                      (f" ... and {len(failed_gists) - 3} more" if len(failed_gists) > 3 else ""))
                total_success = False
            else:
                print("   🎉 All gists processed successfully!")

        print(f"\n💾 BACKUP LOCATION:")
        print(f"   {backup_path}")

        if total_success:
            print(f"\n🎉 SUCCESS: All backup operations completed successfully!")
        else:
            print(f"\n⚠️  WARNING: Some items failed - check logs for details")

        print("=" * 60)

        self.success = True
        return True
