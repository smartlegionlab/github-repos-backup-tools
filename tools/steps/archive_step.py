import os
from datetime import datetime
from typing import Dict, Any
from tools.steps.base import BaseStep
from tools.archive_creator import ArchiveCreator


class ArchiveStep(BaseStep):
    def __init__(self):
        super().__init__(
            name="Archive Creation",
            description="Creating backup archive"
        )

    def execute(self, context: Dict[str, Any]) -> bool:
        print(f"🔧 {self.description}...")

        args = context.get('args', {})
        backup_path = context.get('backup_path')
        github_login = context.get('github_login')

        if not getattr(args, 'archive', False):
            print("⚠️ Archive creation not requested - skipping")
            return True

        if not backup_path:
            print("❌ No backup path found in context")
            return False

        if not os.path.exists(backup_path):
            print("❌ Backup directory does not exist")
            return False

        print("🗄 Creating backup archive...")
        try:
            archive_path = self._create_archive_with_proper_name(backup_path, github_login)
            print(f"✅ Archive created successfully: {archive_path}")
            self.success = True
            return True
        except Exception as e:
            print(f"❌ Failed to create archive: {e}")
            return False

    def _create_archive_with_proper_name(self, backup_path: str, github_login: str = None) -> str:
        if github_login:
            base_name = f"github_{github_login}"
        else:
            base_name = "github_backup"

        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_name = f"{base_name}_{current_time}"

        import tempfile
        import shutil

        temp_dir = tempfile.mkdtemp()
        renamed_backup_path = os.path.join(temp_dir, archive_name)

        try:
            shutil.copytree(backup_path, renamed_backup_path)

            archive_path = ArchiveCreator.create_archive(renamed_backup_path, "zip")

            final_archive_path = self._rename_archive_to_final_name(archive_path, archive_name)

            return final_archive_path

        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    def _rename_archive_to_final_name(self, archive_path: str, archive_name: str) -> str:
        archive_dir = os.path.dirname(archive_path)
        archive_extension = os.path.splitext(archive_path)[1]

        final_name = f"{archive_name}{archive_extension}"
        final_path = os.path.join(archive_dir, final_name)

        os.rename(archive_path, final_path)
        return final_path
