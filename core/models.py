# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
# https://github.com/smartlegionlab/
# --------------------------------------------------------
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


@dataclass
class BackupStats:
    total_repos: int = 0
    cloned: int = 0
    updated: int = 0
    skipped: int = 0
    failed: int = 0
    total_branches: int = 0
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    failed_repos: List[str] = field(default_factory=list)

    @property
    def elapsed_time(self) -> str:
        if self.start_time and self.end_time:
            delta = self.end_time - self.start_time
            return str(delta).split('.')[0]
        return "00:00:00"


@dataclass
class RepoInfo:
    name: str
    full_name: str
    clone_url: str
    default_branch: str
    private: bool
    pushed_at: str
    branches: List[str] = field(default_factory=list)
