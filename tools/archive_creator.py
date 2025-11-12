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
from abc import ABC, abstractmethod
from typing import ClassVar


class BaseArchiveCreator(ABC):

    @classmethod
    @abstractmethod
    def get_extension(cls) -> str:
        pass

    @classmethod
    def create(cls, folder_path: str) -> str:
        output_path = cls._get_output_path(folder_path)
        cls._create_archive(folder_path, output_path)
        return output_path

    @classmethod
    def _get_output_path(cls, folder_path: str) -> str:
        folder_name = os.path.basename(folder_path)
        return os.path.join(os.path.dirname(folder_path), f"{folder_name}.{cls.get_extension()}")

    @classmethod
    @abstractmethod
    def _create_archive(cls, folder_path: str, output_path: str):
        pass

    @classmethod
    def _add_files_to_archive(cls, folder_path: str, add_file_func):
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, folder_path)
                add_file_func(file_path, arc_name)


class ZipArchiveCreator(BaseArchiveCreator):

    @classmethod
    def get_extension(cls) -> str:
        return "zip"

    @classmethod
    def _create_archive(cls, folder_path: str, output_path: str):
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            cls._add_files_to_archive(folder_path, zipf.write)


class TarArchiveCreator(BaseArchiveCreator):

    COMPRESSION_MODES: ClassVar[dict] = {
        '': 'w',
        'gz': 'w:gz',
        'bz2': 'w:bz2',
        'xz': 'w:xz'
    }

    @classmethod
    def get_extension(cls, compression: str = '') -> str:
        extensions = {'': 'tar', 'gz': 'tar.gz', 'bz2': 'tar.bz2', 'xz': 'tar.xz'}
        return extensions.get(compression, 'tar')

    @classmethod
    def create(cls, folder_path: str, compression: str = '') -> str:
        output_path = cls._get_output_path_with_compression(folder_path, compression)
        cls._create_archive(folder_path, output_path, compression)
        return output_path

    @classmethod
    def _get_output_path_with_compression(cls, folder_path: str, compression: str) -> str:
        folder_name = os.path.basename(folder_path)
        extension = cls.get_extension(compression)
        return os.path.join(os.path.dirname(folder_path), f"{folder_name}.{extension}")

    @classmethod
    def _create_archive(cls, folder_path: str, output_path: str, compression: str = ''):
        mode = cls.COMPRESSION_MODES.get(compression, 'w')
        with tarfile.open(output_path, mode) as tarf:
            cls._add_files_to_archive(folder_path, tarf.add)


class ArchiveCreator:

    FORMATS: ClassVar[dict] = {
        'zip': ZipArchiveCreator,
        'tar': TarArchiveCreator,
        'tar.gz': TarArchiveCreator,
        'tgz': TarArchiveCreator,
        'tar.bz2': TarArchiveCreator
    }

    @classmethod
    def create_archive(cls, folder_path: str, archive_format: str = 'zip', **kwargs) -> str:
        creator_class = cls.FORMATS.get(archive_format)
        if not creator_class:
            raise ValueError(f"Unsupported archive format: {archive_format}")

        if creator_class == TarArchiveCreator:
            compression = 'gz' if archive_format in ['tar.gz', 'tgz'] else 'bz2' if archive_format == 'tar.bz2' else ''
            return creator_class.create(folder_path, compression, **kwargs)
        else:
            return creator_class.create(folder_path, **kwargs)
