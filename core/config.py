from pathlib import Path


class Config:
    app_name = 'Github Repositories Backup Tools'
    app_url = 'https://github.com/smartlegionlab/'
    app_copyright = 'Copyright © 2025, Alexander Suvorov'
    app_help_url = 'https://github.com/smartlegionlab/github-repos-backup-tools/'


class ConfigPathManager:
    def __init__(self, dir_name: str = "github_repos_backup_tools"):
        self.dir_name = dir_name
        self.config_dir = self._get_path_dir()

    def _get_path_dir(self) -> Path:
        home = Path.home()
        config_base = home / ".config"
        config_base.mkdir(exist_ok=True)
        app_config_dir = config_base / self.dir_name
        app_config_dir.mkdir(exist_ok=True)
        return app_config_dir
