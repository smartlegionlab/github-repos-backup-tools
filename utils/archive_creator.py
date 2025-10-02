# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# (see LICENSE for details).
# Copyright © 2025, Alexander Suvorov
# All rights reserved.
# --------------------------------------------------------
# https://github.com/smartlegionlab/
# --------------------------------------------------------
import os
import zipfile
import tarfile


class ArchiveCreator:
    def __init__(self, folder_path: str, archive_format: str = 'zip'):
        self.folder_path = folder_path
        self.archive_format = archive_format
        self.output_path = self._default_output_path()

    def _default_output_path(self) -> str:
        folder_name = os.path.basename(self.folder_path)
        return os.path.join(os.path.dirname(self.folder_path), f"{folder_name}.{self.archive_format}")

    def create_archive(self):
        if self.archive_format == 'zip':
            self._create_zip()
        else:
            self._create_tar()

    def _create_zip(self):
        with zipfile.ZipFile(self.output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(self.folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, self.folder_path))
        print(f"\nZIP archive created at: {self.output_path}\n")

    def _create_tar(self):
        mode = 'w:gz' if self.archive_format in ['tar.gz', 'tgz'] else 'w'
        with tarfile.open(self.output_path, mode) as tarf:
            for root, _, files in os.walk(self.folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    tarf.add(file_path, arcname=os.path.relpath(file_path, self.folder_path))
        print(f"\nTar archive created at: {self.output_path}\n")
