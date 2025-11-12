import pytest
import os
import zipfile
import tarfile

from tools.archive_creator import ZipArchiveCreator, TarArchiveCreator, ArchiveCreator


class TestZipArchiveCreator:

    def test_create_zip_archive(self, temp_folder):
        output_path = ZipArchiveCreator.create(str(temp_folder))

        assert os.path.exists(output_path)
        assert output_path.endswith(".zip")

        with zipfile.ZipFile(output_path, 'r') as zipf:
            file_list = zipf.namelist()

            assert "file1.txt" in file_list
            assert "file2.txt" in file_list
            assert "subdir/subfile.txt" in file_list

            with zipf.open("file1.txt") as f:
                content = f.read().decode('utf-8')
                assert content == "Content of file1"

    def test_create_zip_empty_folder(self, empty_folder):
        output_path = ZipArchiveCreator.create(str(empty_folder))

        assert os.path.exists(output_path)

        with zipfile.ZipFile(output_path, 'r') as zipf:
            assert len(zipf.namelist()) == 0


class TestTarArchiveCreator:

    def test_create_tar_archive(self, temp_folder):
        output_path = TarArchiveCreator.create(str(temp_folder), '')

        assert os.path.exists(output_path)
        assert output_path.endswith(".tar")

        with tarfile.open(output_path, 'r') as tarf:
            file_list = tarf.getnames()

            assert "file1.txt" in file_list
            assert "file2.txt" in file_list
            assert "subdir/subfile.txt" in file_list

    def test_create_tar_gz_archive(self, temp_folder):
        output_path = TarArchiveCreator.create(str(temp_folder), 'gz')

        assert os.path.exists(output_path)
        assert output_path.endswith(".tar.gz")

        with tarfile.open(output_path, 'r:gz') as tarf:
            assert len(tarf.getnames()) == 3


class TestArchiveCreatorFacade:

    def test_create_zip_via_facade(self, temp_folder):
        output_path = ArchiveCreator.create_archive(str(temp_folder), "zip")

        assert os.path.exists(output_path)
        assert output_path.endswith(".zip")

        with zipfile.ZipFile(output_path, 'r') as zipf:
            assert len(zipf.namelist()) == 3

    def test_create_tar_via_facade(self, temp_folder):
        output_path = ArchiveCreator.create_archive(str(temp_folder), "tar")

        assert os.path.exists(output_path)
        assert output_path.endswith(".tar")

        with tarfile.open(output_path, 'r') as tarf:
            assert len(tarf.getnames()) == 3

    def test_create_tar_gz_via_facade(self, temp_folder):
        output_path = ArchiveCreator.create_archive(str(temp_folder), "tar.gz")

        assert os.path.exists(output_path)
        assert output_path.endswith(".tar.gz")

        with tarfile.open(output_path, 'r:gz') as tarf:
            assert len(tarf.getnames()) == 3

    def test_default_format_is_zip(self, temp_folder):
        output_path = ArchiveCreator.create_archive(str(temp_folder))

        assert output_path.endswith(".zip")
        assert os.path.exists(output_path)

    def test_unsupported_format_raises_error(self, temp_folder):
        with pytest.raises(ValueError, match="Unsupported archive format"):
            ArchiveCreator.create_archive(str(temp_folder), "rar")
