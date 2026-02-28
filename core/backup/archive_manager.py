# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
# https://github.com/smartlegionlab/
# --------------------------------------------------------
import os
import zipfile
from pathlib import Path
from datetime import datetime
from typing import Optional

from core.config.settings import ProjectPaths


class ArchiveManager:

    def __init__(self, username: str):
        self.username = username
        self.user_dir = ProjectPaths.get_user_dir(username)
        self.repos_dir = ProjectPaths.get_repos_dir(username)

    def create_archive(self) -> Optional[Path]:
        print("\n📦 Archive Creation")

        if not self.repos_dir.exists():
            print("   ❌ Repositories directory does not exist")
            return None

        try:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            archive_name = f"{self.username}_github_backup_{timestamp}"
            archive_path = self.user_dir / f"{archive_name}.zip"

            print(f"   Creating archive: {archive_name}.zip")
            print(f"   From: {self.repos_dir}")
            print(f"   To: {archive_path}")

            with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, _, files in os.walk(self.repos_dir):
                    for file in files:
                        file_path = Path(root) / file
                        arc_name = f"repositories/{file_path.relative_to(self.repos_dir)}"
                        zipf.write(file_path, arc_name)

            size_mb = archive_path.stat().st_size / (1024 * 1024)
            print(f"   ✅ Archive created successfully!")
            print(f"   📊 Size: {size_mb:.2f} MB")
            print(f"   📁 Location: {archive_path}")

            return archive_path

        except Exception as e:
            print(f"   ❌ Archive creation failed: {e}")
            return None
