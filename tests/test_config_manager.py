import tempfile

from pathlib import Path
from unittest.mock import patch

from tools.config_manager import ConfigManager


class TestConfigManager:

    def test_init_creates_correct_paths(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            with patch.object(Path, 'home', return_value=temp_path):
                manager = ConfigManager("test_app")

                expected_config_dir = temp_path / ".config" / "test_app"
                expected_token_file = expected_config_dir / "github_token.json"
                expected_config_file = expected_config_dir / "config.json"

                assert manager.config_dir == expected_config_dir
                assert manager.token_file == expected_token_file
                assert manager.config_file == expected_config_file

    def test_token_validation(self):
        assert ConfigManager.validate_token_format("ghp_abc123def456") == True
        assert ConfigManager.validate_token_format("github_pat_abc123") == True

        assert ConfigManager.validate_token_format("") == False
        assert ConfigManager.validate_token_format("abc") == False
        assert ConfigManager.validate_token_format("invalid@token!") == False

    def test_save_and_load_token(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            with patch.object(Path, 'home', return_value=temp_path):
                manager = ConfigManager("test_app")
                test_token = "ghp_testtoken123456"

                result = manager.save_token(test_token)
                assert result == True
                assert manager.token_file.exists()

                loaded_token = manager.load_token()
                assert loaded_token == test_token

    def test_token_exists(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            with patch.object(Path, 'home', return_value=temp_path):
                manager = ConfigManager("test_app")

                assert manager.token_exists() == False

                manager.save_token("ghp_testtoken")
                assert manager.token_exists() == True

    def test_get_or_request_token_existing(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            with patch.object(Path, 'home', return_value=temp_path):
                manager = ConfigManager("test_app")
                test_token = "ghp_existingtoken"

                manager.save_token(test_token)

                with patch('builtins.print'):
                    token = manager.get_or_request_token()
                    assert token == test_token

    def test_get_or_request_token_new(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            with patch.object(Path, 'home', return_value=temp_path):
                manager = ConfigManager("test_app")
                test_token = "ghp_newtoken123"

                with patch('getpass.getpass', return_value=test_token), \
                        patch('builtins.print'):
                    token = manager.get_or_request_token()
                    assert token == test_token
                    assert manager.token_exists() == True

    def test_save_and_load_config(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            with patch.object(Path, 'home', return_value=temp_path):
                manager = ConfigManager("test_app")
                test_config = {"setting1": "value1", "setting2": 42}

                result = manager.save_config(test_config)
                assert result == True
                assert manager.config_file.exists()

                loaded_config = manager.load_config()
                assert loaded_config == test_config

    def test_load_config_missing_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            with patch.object(Path, 'home', return_value=temp_path):
                manager = ConfigManager("test_app")

                config = manager.load_config()
                assert config == {}
