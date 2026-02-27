# --------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# Copyright (©) 2026, Alexander Suvorov. All rights reserved.
# https://github.com/smartlegionlab/
# --------------------------------------------------------
from dataclasses import dataclass
from typing import Optional


@dataclass
class UserInfo:
    login: str
    name: Optional[str]
    email: Optional[str]
    public_repos: int
    private_repos: int
    followers: int
    following: int
    created_at: str
    updated_at: str
