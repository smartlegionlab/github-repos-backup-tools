# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# (see LICENSE for details).
# Copyright © 2025, Alexander Suvorov
# All rights reserved.
# --------------------------------------------------------
# https://github.com/smartlegionlab/
# --------------------------------------------------------

class ReportManager:
    def __init__(self, github_client, backup_path, failed_repos, failed_gists, repo_flag=False, gists_flag=False):
        self.github_client = github_client
        self.backup_path = backup_path
        self.failed_repos = failed_repos or {}
        self.failed_gists = failed_gists or {}
        self.total_success = True
        self.repo_flag = repo_flag
        self.gists_flag = gists_flag

    def execute(self):
        try:
            if self.repo_flag:
                total_repos = len(self.github_client.repositories)
                successful_repos = total_repos - len(self.failed_repos)

                print(f"\n📦 REPOSITORIES:")
                print(f"   Total: {total_repos}")
                print(f"   ✅ Successful: {successful_repos}")
                print(f"   ❌ Failed: {len(self.failed_repos)}")

                if self.failed_repos:
                    print(f"   Failed items: {', '.join(list(self.failed_repos.keys())[:3])}" +
                          (f" ... and {len(self.failed_repos) - 3} more" if len(self.failed_repos) > 3 else ""))
                    self.total_success = False
                else:
                    print("   🎉 All repositories processed successfully!")

            if self.gists_flag:
                total_gists = len(self.github_client.gists)
                successful_gists = total_gists - len(self.failed_gists)

                print(f"\n📝 GISTS:")
                print(f"   Total: {total_gists}")
                print(f"   ✅ Successful: {successful_gists}")
                print(f"   ❌ Failed: {len(self.failed_gists)}")

                if self.failed_gists:
                    print(f"   Failed items: {', '.join(list(self.failed_gists.keys())[:3])}" +
                          (f" ... and {len(self.failed_gists) - 3} more" if len(self.failed_gists) > 3 else ""))
                    self.total_success = False
                else:
                    print("   🎉 All gists processed successfully!")

            print(f"\n💾 BACKUP LOCATION:")
            print(f"   {self.backup_path}")

            if self.total_success:
                print(f"\n🎉 SUCCESS: All backup operations completed successfully!")
            else:
                print(f"\n⚠️  WARNING: Some items failed - check logs for details")

            print("=" * 60)
        except Exception as e:
            print(e)
            return False
        return True
