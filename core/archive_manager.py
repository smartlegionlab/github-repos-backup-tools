import os
import shutil
from datetime import datetime

from core.archive_creator import ArchiveCreator


class ArchiveManager:

    def __init__(self, backup_path, github_login):
        self.backup_path = backup_path
        self.github_login = github_login

    def execute(self):
        if not self.backup_path:
            print("❌ No backup path found in context")
            return False

        if not os.path.exists(self.backup_path):
            print("❌ Backup directory does not exist")
            return False

        print("Creating backup archive...")

        try:
            archive_path = self._create_archive_in_home(self.backup_path, self.github_login)
            print(f"✅ Archive created successfully: {archive_path}")
            return True
        except Exception as e:
            print(f"❌ Failed to create archive: {e}")
            return False

    def _create_archive_in_home(self, backup_path: str, github_login: str = None) -> str:

        if github_login:
            base_name = f"github_{github_login}"
        else:
            base_name = "github_backup"

        current_time = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
        archive_name = f"{base_name}_{current_time}"

        home_directory = os.path.expanduser('~')
        final_archive_path = os.path.join(home_directory, f"{archive_name}.zip")

        import tempfile

        temp_dir = tempfile.mkdtemp()
        renamed_backup_path = os.path.join(temp_dir, archive_name)

        try:
            shutil.copytree(backup_path, renamed_backup_path)

            archive_path = ArchiveCreator.create_archive(renamed_backup_path, "zip")

            shutil.move(archive_path, final_archive_path)
            return final_archive_path

        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
