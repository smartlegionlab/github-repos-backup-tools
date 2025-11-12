import pytest
import tempfile
from pathlib import Path


@pytest.fixture
def temp_folder():
    with tempfile.TemporaryDirectory() as temp_dir:
        test_dir = Path(temp_dir)

        subdir = test_dir / "subdir"
        subdir.mkdir()

        (test_dir / "file1.txt").write_text("Content of file1")
        (test_dir / "file2.txt").write_text("Content of file2")
        (subdir / "subfile.txt").write_text("Content of subfile")

        yield test_dir


@pytest.fixture
def empty_folder():
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)
