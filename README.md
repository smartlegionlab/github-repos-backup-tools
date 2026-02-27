# GitHub Repositories Backup Tools <sup>v1.5.0</sup>

A professional solution for automatic cloning and backup of all your GitHub repositories.

---

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/smartlegionlab/github-repos-backup-tools)](https://github.com/smartlegionlab/github-repos-backup-tools/releases)
![GitHub top language](https://img.shields.io/github/languages/top/smartlegionlab/github-repos-backup-tools)
[![GitHub](https://img.shields.io/github/license/smartlegionlab/github-repos-backup-tools)](https://github.com/smartlegionlab/github-repos-backup-tools/blob/master/LICENSE)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![Platform](https://img.shields.io/badge/platform-windows%20%7C%20linux%20%7C%20macos-lightgrey)
![GitHub last commit](https://img.shields.io/github/last-commit/smartlegionlab/github-repos-backup-tools)

---

**You can also use my other projects to work with repositories:**

- [Smart Repository Manager GUI](https://github.com/smartlegionlab/smart-repository-manager-gui)
  A powerful desktop application for managing GitHub repositories with intelligent synchronization, SSH configuration, and comprehensive visual management tools.
- [Smart Repository Manager CLI](https://github.com/smartlegionlab/smart-repository-manager-cli)
  A comprehensive command-line tool for managing GitHub repositories with advanced synchronization, SSH configuration management, and intelligent local repository management.
- [Smart Repository Manager Core](https://github.com/smartlegionlab/smart-repository-manager-core)
  A Python library for managing Git repositories with intelligent synchronization, SSH configuration validation, and GitHub integration.

---

## 🚀 Features

- **Full Backup** - clones ALL repositories (public and private) from your account and organizations
- **All Branches** - automatically creates local branches for ALL remote branches
- **Smart Update** - compares local commits with GitHub, updates only when needed
- **Automatic Retries** - up to 5 attempts with exponential backoff on failures
- **Health Check** - automatic integrity verification of each repository
- **No SSH Required** - uses only HTTPS with token authentication
- **Token Persistence** - token is saved after first use and reused on subsequent runs
- **Progress with Error Counter** - visual progress bar showing current/total/errors
- **Detailed Report** - statistics on cloned/updated/synced/skipped/failed repositories
- **Branch Pruning** - automatically removes local branches deleted on remote
- **Archiving** - creates timestamped ZIP archive in the application folder
- **Power Management** - shutdown/reboot after completion (optional)
- **Fast Mode** - `--no-branches` flag to skip branch synchronization for speed

## 📁 Structure

```
~/github_backup_repos_tools/              # Main application folder
└── username/                              # Your GitHub username
    ├── repositories/                       # All cloned repositories
    │   ├── repo1/                          # Full copy with ALL branches
    │   ├── repo2/
    │   └── ...
    └── config.json                          # Token file (automatically created)
```

## 🖥 System Requirements

- **Python**: 3.8+ (standard library only, no external dependencies)
- **Git**: 2.20+
- **Storage**: depends on repository sizes
- **Network**: stable internet connection

## 🚀 Quick Start

### 1. Installation
```bash
git clone https://github.com/smartlegionlab/github-repos-backup-tools.git
cd github-repos-backup-tools
```

### 2. First Run
```bash
python app.py -r
```
On first run, the program will ask for your GitHub token and save it.

### 3. Get GitHub Token
1. Go to [GitHub Tokens](https://github.com/settings/tokens/new)
2. Select permissions:
   - ✅ `repo` (full repository access)
   - ✅ `read:org` (access to organization repositories)
3. Generate and copy the token

## 💻 Usage

### Basic Commands
| Command | Description |
|---------|-------------|
| `-r` | Clone/update repositories |
| `-t` | Update token (delete old and request new) |
| `--no-archive` | Disable archive creation (archive is created by default) |
| `--timeout N` | Timeout for Git operations in seconds (default: 30) |
| `--no-branches` | Disable branch synchronization (faster, only default branch) |

### Power Management
| Command | Description |
|---------|-------------|
| `--shutdown` | Shutdown computer after completion |
| `--reboot` | Reboot computer after completion |

### Usage Examples
```bash
# Full backup with all branches (default)
python app.py -r

# Fast mode - only default branch, no branch sync
python app.py -r --no-branches

# Backup without archive
python app.py -r --no-archive

# With increased timeout
python app.py -r --timeout 60

# Update token
python app.py -t

# Backup with shutdown
python app.py -r --shutdown
```

## 📊 Example Output

```
********************************************************************************
----------------------- GitHub Repositories Backup Tools -----------------------

🔧 Arguments Parsing:
Parsed arguments:
   Backup: Repositories, Archive
   Timeout: 30s
   Branches: ✅ Enabled
   Power: ❌ No action

📁 Application Setup
   Application directory: /home/user/github_backup_repos_tools

🌐 Network Check
✅ Internet connection OK
✅ GitHub accessible

🔐 GitHub Authentication
   Found existing user: smartlegionlab
✅ Authenticated as: smartlegionlab

🔍 Scanning repositories...
📦 Fetching all repositories...
   ✅ Found 52 repositories

📁 Backup location: /home/user/github_backup_repos_tools/smartlegionlab
   Repositories: /home/user/github_backup_repos_tools/smartlegionlab/repositories

📂 Processing 52 repositories...
   Branch sync: ✅ Enabled

[██████████████████████████████] 100.0% | 52/52/0 | SYNC | smartlegionlab/repo
✅ Repository processing complete!

============================================================
📋 BACKUP REPORT
============================================================
👤 User: smartlegionlab
📁 Application directory: /home/user/github_backup_repos_tools
   └─ smartlegionlab/
       ├─ repositories/
       └─ config.json

⏱️  Started: 2026-02-27 17:19:01
⏱️  Finished: 2026-02-27 17:24:20
⏱️  Duration: 0:05:18

📊 REPOSITORY STATISTICS:
   Total:           52 repositories
   ✅ Cloned:          0 repositories (new)
   🔄 Updated:         0 repositories
   🔄 Synced:         52 repositories (branches only)
   ❌ Failed:          0 repositories
   📚 Branches:      245 total

📈 Success rate: 100.0%

============================================================
✅ ALL REPOSITORIES BACKED UP SUCCESSFULLY!
============================================================

📦 Archive Creation
   ✅ Archive created: smartlegionlab_github_backup_2026-02-27_17-24-20.zip
   📊 Size: 15.19 MB
------------------------------------------------------------------------------------
------------------------ https://github.com/smartlegionlab/ ------------------------
----------------------- Copyright © 2026, Alexander Suvorov ------------------------
************************************************************************************
```

## 🔄 How It Works

### Operation Modes

| Mode | Command | CLONE | PULL | SYNC | SKIP |
|------|---------|-------|------|------|------|
| **Default** | `python app.py -r` | Full + branches | Code + branches | Branches only | - |
| **Fast** | `python app.py -r --no-branches` | Full + branches | Code only | - | Nothing |

### Update Logic

1. **Quick check**: compare local commit date with GitHub pushed_at
2. **If difference > 5 minutes**: compare actual commit hashes via `ls-remote`
3. **If hashes differ**: perform `git pull`
4. **After pull**: verify repository health with `git rev-parse HEAD`
5. **If corrupted**: automatic re-clone with retries

### Branch Synchronization (Default Mode)

- **CLONE**: creates local branches for all remote branches
- **PULL**: fetches all branches + updates code + creates new branches
- **SYNC**: fetches all branches + creates new branches + prunes deleted ones
- **Pruning**: automatically removes local branches deleted on remote

## 🔒 Security

- Token stored in `~/github_backup_repos_tools/[username]/config.json`
- Uses HTTPS with token in URL (not transmitted in plain text)
- Path traversal attack protection
- No telemetry or third-party data transmission
- Token can be updated with `-t` command

## ⚠️ Known Limitations

- **Gists not supported** - utility works with repositories only
- **Git required** - must be installed on the system
- **Token permissions** - requires `repo` and `read:org`

## 🛠 Troubleshooting

**Q: Authentication fails?**  
A: Verify token has `repo` and `read:org` permissions. Use `-t` to update.

**Q: Clone timeout?**  
A: Increase timeout: `--timeout 60`

**Q: Where is token stored?**  
A: In `~/github_backup_repos_tools/[username]/config.json`

**Q: How to cancel scheduled shutdown?**  
A: `shutdown -c` (Linux/macOS) or `shutdown /a` (Windows)

**Q: Fast mode still slow?**  
A: Fast mode skips branch sync, but still does health checks and hash verification when needed

---

## 🚀 What's New in v1.5.0

- ✅ **New folder structure** - `~/github_backup_repos_tools/[username]/repositories/`
- ✅ **All branches** - creates local branches for ALL remote branches
- ✅ **Branch pruning** - automatically removes local branches deleted on remote
- ✅ **No SSH required** - uses only HTTPS with token authentication
- ✅ **Smart update** - two-stage verification (date + hash) before pull
- ✅ **Health checks** - verifies repository integrity after each operation
- ✅ **Automatic recovery** - re-clones corrupted repositories
- ✅ **Exponential backoff** - up to 5 retries with increasing delays
- ✅ **Fast mode** - new `--no-branches` flag for speed

### Two Operation Modes

| Mode | Command | Behavior | Use Case |
|------|---------|----------|----------|
| **Default** | `python app.py -r` | Full backup with ALL branches | Complete backup |
| **Fast** | `python app.py -r --no-branches` | Code only, no branch sync | Quick daily sync |

### Performance Comparison
- **Default mode**: ~3-5 seconds per repository (with branches)
- **Fast mode**: ~1-2 seconds per repository (code only)
- **SKIP** (no changes): virtually instant

---

**Author**: Alexander Suvorov  
**License**: [BSD 3-Clause License](https://github.com/smartlegionlab/github-repos-backup-tools/blob/master/LICENSE)  
**Support**: [GitHub Issues](https://github.com/smartlegionlab/github-repos-backup-tools/issues)  
**Source Code**: [https://github.com/smartlegionlab/](https://github.com/smartlegionlab/github-repos-backup-tools)

---

<div align="center">

**⭐ Star this repo if you find it useful!**

</div>