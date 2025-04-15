# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# (see LICENSE for details).
# Copyright © 2018-2025, A.A. Suvorov
# All rights reserved.
# --------------------------------------------------------
# https://github.com/smartlegionlab/
# --------------------------------------------------------
import os
from typing import Dict


class BackupReporter:
    @staticmethod
    def _generate_item_report(
            item_type: str,
            icon: str,
            data: Dict[str, str],
            failed_items: Dict[str, str],
            max_errors_to_show: int = 3
    ) -> list:
        report_lines = []
        total = len(data)
        success = total - len(failed_items)
        status = "✅" if not failed_items else "⚠️"

        report_lines.append(f"║ {icon} {item_type.capitalize()}: {success}/{total} cloned {status}")

        if failed_items:
            report_lines.append(f"║ Failed {item_type}:")
            for item_name in list(failed_items.keys())[:max_errors_to_show]:
                shortened_name = f"{item_name[:40]}..." if len(item_name) > 40 else item_name
                report_lines.append(f"║   - {shortened_name}")

            if len(failed_items) > max_errors_to_show:
                report_lines.append(f"║   + {len(failed_items) - max_errors_to_show} more...")

        return report_lines

    @staticmethod
    def _generate_archive_report(backup_path: str) -> list:
        archive_exists = os.path.exists(f"{backup_path}.zip")
        status = "✅" if archive_exists else "⚠️"
        return [f"║ 🗄 Archive: {'Created' if archive_exists else 'Failed'} {status}"]

    @staticmethod
    def generate(
            clone_repos: bool,
            clone_gists: bool,
            make_archive: bool,
            repos_data: Dict[str, str],
            gists_data: Dict[str, str],
            failed_repos: Dict[str, str],
            failed_gists: Dict[str, str],
            backup_path: str
    ) -> str:
        try:
            failed_repos = failed_repos or {}
            failed_gists = failed_gists or {}
            repos_data = repos_data or {}
            gists_data = gists_data or {}

            report = []

            if clone_repos:
                report.extend(
                    BackupReporter._generate_item_report(
                        item_type="repos",
                        icon="📦",
                        data=repos_data,
                        failed_items=failed_repos
                    )
                )

            if clone_gists:
                report.extend(
                    BackupReporter._generate_item_report(
                        item_type="gists",
                        icon="📝",
                        data=gists_data,
                        failed_items=failed_gists
                    )
                )

            if make_archive:
                report.extend(BackupReporter._generate_archive_report(backup_path))

            return "\n".join(report)

        except Exception as e:
            return f"\n⚠️ Error generating report: {e}\n"
