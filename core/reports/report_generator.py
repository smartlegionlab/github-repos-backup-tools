# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
# https://github.com/smartlegionlab/
# --------------------------------------------------------
from datetime import datetime
from typing import Dict, Any

from core.config.settings import ProjectPaths
from core.github.api_client import GitHubAPIClient
from core.models import BackupStats


class ReportGenerator:

    def __init__(self, github_client: GitHubAPIClient, stats: BackupStats):
        self.github_client = github_client
        self.username = github_client.login
        self.stats = stats
        self.user_dir = ProjectPaths.get_user_dir(self.username)
        self.repos_dir = ProjectPaths.get_repos_dir(self.username)

    def generate(self) -> Dict[str, Any]:
        print("\n" + "=" * 60)
        print("📋 BACKUP REPORT")
        print("=" * 60)

        print(f"👤 User: {self.github_client.login}")
        print(f"📁 Application directory: {ProjectPaths.get_app_dir()}")
        print(f"   └─ {self.username}/")
        print(f"       ├─ repositories/")
        print(f"       └─ config.json")
        print(
            f"\n⏱️  Started: {self.stats.start_time.strftime('%Y-%m-%d %H:%M:%S') if self.stats.start_time else 'N/A'}")
        print(f"⏱️  Finished: {self.stats.end_time.strftime('%Y-%m-%d %H:%M:%S') if self.stats.end_time else 'N/A'}")
        print(f"⏱️  Duration: {self.stats.elapsed_time}")

        print("\n📊 REPOSITORY STATISTICS:")
        print(f"   {'Total:':15} {self.stats.total_repos:4} repositories")
        print(f"   {'✅ Cloned:':15} {self.stats.cloned:4} repositories (new)")
        print(f"   {'🔄 Updated:':15} {self.stats.updated:4} repositories")
        print(f"   {'🔄 Synced:':15} {self.stats.synced:4} repositories (branches only)")
        print(f"   {'❌ Failed:':15} {self.stats.failed:4} repositories")
        print(f"   {'📚 Branches:':15} {self.stats.total_branches:4} total")

        if self.stats.total_repos > 0:
            success_rate = ((self.stats.total_repos - self.stats.failed) / self.stats.total_repos * 100)
            print(f"\n📈 Success rate: {success_rate:.1f}%")

        if self.stats.failed_repos:
            print(f"\n❌ FAILED REPOSITORIES ({len(self.stats.failed_repos)}):")
            for i, repo in enumerate(self.stats.failed_repos[:10], 1):
                print(f"   {i}. {repo}")
            if len(self.stats.failed_repos) > 10:
                print(f"   ... and {len(self.stats.failed_repos) - 10} more")

        print("\n" + "=" * 60)
        if self.stats.failed == 0:
            print("✅ ALL REPOSITORIES BACKED UP SUCCESSFULLY!")
        else:
            print(f"⚠️  Backup completed with {self.stats.failed} failures")
        print("=" * 60)

        return {
            "timestamp": datetime.now().isoformat(),
            "user": self.github_client.login,
            "app_directory": str(ProjectPaths.get_app_dir()),
            "user_directory": str(self.user_dir),
            "repositories_directory": str(self.repos_dir),
            "stats": {
                "total": self.stats.total_repos,
                "cloned": self.stats.cloned,
                "updated": self.stats.updated,
                "synced": self.stats.synced,
                "failed": self.stats.failed,
                "total_branches": self.stats.total_branches,
                "failed_repos": self.stats.failed_repos,
                "duration_seconds": (self.stats.end_time - self.stats.start_time).total_seconds()
                if self.stats.start_time and self.stats.end_time else 0,
                "success_rate": ((self.stats.total_repos - self.stats.failed) / self.stats.total_repos * 100)
                if self.stats.total_repos > 0 else 0
            }
        }
