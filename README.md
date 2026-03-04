# GitHub Repositories Backup Tools <sup>v1.6.1</sup>

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
- **Smart Update** - compares local commits with GitHub, updates only when needed
- **Automatic Retries** - up to 5 attempts with exponential backoff on failures
- **Health Check** - automatic integrity verification of each repository
- **No SSH Required** - uses only HTTPS with token authentication
- **Token Persistence** - token is saved after first use and reused on subsequent runs
- **Progress with Error Counter** - visual progress bar showing current/total/errors
- **Detailed Report** - statistics on cloned/updated/synced/skipped/failed repositories
- **User Profile Export** - saves GitHub user information to `user_info.json`
- **Branch Pruning** - automatically removes local branches deleted on remote (Full Mode)
- **Organized Backups** - all archives and reports stored in `backups/` folder
- **Power Management** - shutdown/reboot after completion (optional)
- **Fast Mode (Default)** - clones only default branch for maximum speed
- **Full Mode** - `--all-branches` flag to enable synchronization of ALL branches

## 📁 Structure

```
~/github_repos_backup_tools/              # Main application folder
└── username/                              # Your GitHub username
    ├── repositories/                       # All cloned repositories
    │   ├── repo1/                          # Repository copy
    │   ├── repo2/
    │   └── ...
    ├── backups/                            # All backup artifacts
    │   ├── backup_report_2026-02-28_15-30-45.json
    │   └── username_github_backup_2026-02-28_15-30-45.zip
    ├── config.json                          # Token file (automatically created)
    └── user_info.json                       # Your GitHub profile information
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
| `--all-branches` | Enable full branch synchronization (slower, clones ALL branches) |

### Power Management
| Command | Description |
|---------|-------------|
| `--shutdown` | Shutdown computer after completion |
| `--reboot` | Reboot computer after completion |

### Usage Examples
```bash
# Fast mode - only default branch (DEFAULT)
python app.py -r

# Full mode - ALL branches (slower but complete)
python app.py -r --all-branches

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
   Branches: ⚡ Fast mode (default branch only)
   Power: ❌ No action

📁 Application Setup
   Application directory: /home/user/github_repos_backup_tools

🌐 Network Check
✅ Internet connection OK
✅ GitHub accessible

🔐 GitHub Authentication
   Found existing user: smartlegionlab
✅ Authenticated as: smartlegionlab

🔍 Scanning repositories...
📦 Fetching all repositories...
   ✅ Found 52 repositories

📄 Saving user information...
   ✅ User info saved: /home/user/github_repos_backup_tools/smartlegionlab/user_info.json

📁 Backup location: /home/user/github_repos_backup_tools/smartlegionlab
   Repositories: /home/user/github_repos_backup_tools/smartlegionlab/repositories

📂 Processing 52 repositories...
   Mode: ⚡ Fast mode (default branch only)

[██████████████████████████████] 100.0% | 52/52/0 | SKIP | smartlegionlab/repo
✅ Repository processing complete!

============================================================
📋 BACKUP REPORT
============================================================
👤 User: smartlegionlab
📁 Application directory: /home/user/github_repos_backup_tools
   └─ smartlegionlab/
       ├─ repositories/
       ├─ backups/
       ├─ config.json
       └─ user_info.json

⏱️  Started: 2026-02-27 17:19:01
⏱️  Finished: 2026-02-27 17:24:20
⏱️  Duration: 0:05:18

📊 REPOSITORY STATISTICS:
   Total:           52 repositories
   ✅ Cloned:          0 repositories (new)
   🔄 Updated:         0 repositories
   🔄 Synced:          0 repositories (branches only)
   ⏭️ Skipped:        52 repositories (no changes)
   ❌ Failed:          0 repositories
   📚 Branches:       52 total

📈 Success rate: 100.0%

============================================================
✅ ALL REPOSITORIES BACKED UP SUCCESSFULLY!
============================================================

📄 JSON report saved: /home/user/github_repos_backup_tools/smartlegionlab/backups/backup_report_2026-02-27_17-24-20.json

📦 Archive Creation
   Creating archive: smartlegionlab_github_backup_2026-02-27_17-24-20.zip
   From: /home/user/github_repos_backup_tools/smartlegionlab/repositories
   To: /home/user/github_repos_backup_tools/smartlegionlab/backups/smartlegionlab_github_backup_2026-02-27_17-24-20.zip
   ✅ Archive created successfully!
   📊 Size: 15.19 MB
------------------------------------------------------------------------------------
------------------------ https://github.com/smartlegionlab/ ------------------------
----------------------- Copyright © 2026, Alexander Suvorov ------------------------
************************************************************************************
```

## 🔄 How It Works

### Operation Modes

#### Fast Mode (Default) - `python app.py -r`
| Action | When it happens | What it does |
|--------|-----------------|--------------|
| **CLONE** | New repository | Full clone (all branches on first clone) |
| **PULL** | Has changes | Updates only code in current branch |
| **SKIP** | No changes | Skips the repository |

#### Full Mode - `python app.py -r --all-branches`
| Action | When it happens | What it does |
|--------|-----------------|--------------|
| **CLONE** | New repository | Full clone (all branches) |
| **PULL** | Has changes | Updates code + all branches |
| **SYNC** | No changes | Only syncs branches (fetch + create local branches) |
| **CLONE (recover)** | Fetch failed | Re-clones the repository |

### Status Meanings in Logs:

| Status | Mode | Meaning |
|--------|------|---------|
| **CLONE** | Both | New repository - full clone |
| **PULL** | Fast | Code update (current branch only) |
| **PULL** | Full | Code + all branches update |
| **SKIP** | Fast | Skipped - no changes |
| **SYNC** | Full | Branch sync only - code hasn't changed |
| **CLONE (recover)** | Full | Re-clone on error |

### User Information Export

Each run saves your GitHub profile information to `user_info.json`:
- Login, name, email, bio
- Public/private repository counts
- Followers and following
- Account creation and update timestamps
- Last backup timestamp

### Backup Organization

All backup artifacts are neatly organized:
- **JSON reports** - `backups/backup_report_*.json`
- **ZIP archives** - `backups/username_github_backup_*.zip`

This keeps your user folder clean and makes it easy to find all backups.

### Update Logic

1. **Quick check**: compare local commit date with GitHub pushed_at
2. **If difference > 5 minutes**: compare actual commit hashes via `ls-remote`
3. **If hashes differ**: perform `git pull`
4. **After pull**: verify repository health with `git rev-parse HEAD`
5. **If corrupted**: automatic re-clone with retries

### Branch Synchronization (Full Mode with `--all-branches`)

- **CLONE**: creates local branches for all remote branches
- **PULL**: fetches all branches + updates code + creates new branches
- **SYNC**: fetches all branches + creates new branches + prunes deleted ones
- **Pruning**: automatically removes local branches deleted on remote

### Fast Mode (Default, without `--all-branches`)

- **CLONE**: clones all branches (first time only)
- **PULL**: updates only the current branch
- **SKIP**: if no changes detected, no operation performed
- **No branch sync after clone**: significantly faster for large repositories with many branches

## 🔒 Security

- Token stored in `~/github_repos_backup_tools/[username]/config.json`
- Uses HTTPS with token in URL (not transmitted in plain text)
- Path traversal attack protection
- No telemetry or third-party data transmission
- Token can be updated with `-t` command
- Archives contain ONLY repositories, no tokens or configs

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
A: In `~/github_repos_backup_tools/[username]/config.json`

**Q: Where are backups stored?**  
A: All archives and reports are in `~/github_repos_backup_tools/[username]/backups/`

**Q: What's in user_info.json?**  
A: Your GitHub profile information - login, name, email, repo counts, followers, etc.

**Q: How to cancel scheduled shutdown?**  
A: `shutdown -c` (Linux/macOS) or `shutdown /a` (Windows)

**Q: Why do I see SKIP for some repos?**  
A: In Fast Mode, repos without changes are skipped to save time.

**Q: What's the difference between SYNC and PULL in Full Mode?**  
A: PULL updates code + branches, SYNC only syncs branches (when code hasn't changed).

---

## 🚀 What's New in v1.6.1

- ✅ **User profile export** - saves GitHub user info to `user_info.json`
- ✅ **Organized backups** - all archives and reports in `backups/` folder
- ✅ **Cleaner archives** - ZIP contains only repositories, no configs or tokens
- ✅ **Improved structure** - `~/github_repos_backup_tools/[username]/backups/`
- ✅ **Branch pruning** - automatically removes local branches deleted on remote
- ✅ **No SSH required** - uses only HTTPS with token authentication
- ✅ **Smart update** - two-stage verification (date + hash) before pull
- ✅ **Health checks** - verifies repository integrity after each operation
- ✅ **Automatic recovery** - re-clones corrupted repositories
- ✅ **Exponential backoff** - up to 5 retries with increasing delays
- ✅ **Two operation modes** - Fast (default) and Full (--all-branches)
- ✅ **SKIP status** - clearly shows when repos are skipped (Fast Mode)
- ✅ **SYNC status** - shows branch-only sync (Full Mode)

### Two Operation Modes

| Mode | Command | Behavior | Use Case |
|------|---------|----------|----------|
| **Fast (Default)** | `python app.py -r` | Code only, default branch after clone | Quick daily sync |
| **Full** | `python app.py -r --all-branches` | Full backup with ALL branches + sync | Complete backup |

### Performance Comparison
- **Fast mode (Default)**: ~1-2 seconds per repository (SKIP when no changes)
- **Full mode**: ~3-5 seconds per repository (always syncs branches)
- **SKIP** (no changes): virtually instant

---

**Author**: Alexander Suvorov  
**License**: [BSD 3-Clause License](https://github.com/smartlegionlab/github-repos-backup-tools/blob/master/LICENSE)  
**Support**: [GitHub Issues](https://github.com/smartlegionlab/github-repos-backup-tools/issues)  
**Source Code**: [https://github.com/smartlegionlab/](https://github.com/smartlegionlab/github-repos-backup-tools)

---

## ⚠️ DISCLAIMER

### COMPLETE AND UNCONDITIONAL WAIVER OF LIABILITY

**BY USING, DOWNLOADING, INSTALLING, COMPILING, OR OTHERWISE INTERACTING WITH THIS SOFTWARE (THE "SOFTWARE"), YOU (THE "USER") EXPRESSLY AND IRREVOCABLY AGREE TO THE FOLLOWING TERMS:**

#### 1. ABSOLUTE WAIVER OF LIABILITY

THE AUTHOR, COPYRIGHT HOLDER, AND CONTRIBUTORS (COLLECTIVELY, THE "AUTHOR") SHALL NOT BE HELD LIABLE UNDER ANY CIRCUMSTANCES, WHETHER IN CONTRACT, TORT (INCLUDING NEGLIGENCE), STRICT LIABILITY, OR ANY OTHER LEGAL OR EQUITABLE THEORY, FOR ANY:

- DIRECT, INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR EXEMPLARY DAMAGES
- LOSS OF PROFITS, REVENUE, OR DATA
- LOSS OF BUSINESS OPPORTUNITY OR GOODWILL
- SYSTEM FAILURE OR MALFUNCTION
- CORRUPTION OR LOSS OF FILES OR DATA
- UNAUTHORIZED ACCESS TO OR DELETION OF FILES
- HARDWARE DAMAGE OR FAILURE
- ANY OTHER DAMAGES OR LOSSES WHATSOEVER

**THIS WAIVER APPLIES EVEN IF THE AUTHOR HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.**

#### 2. UNCONDITIONAL ACCEPTANCE OF RISK

THE USER ACKNOWLEDGES AND ACCEPTS THAT:

- THE SOFTWARE IS PROVIDED "AS IS" AND "AS AVAILABLE" WITHOUT ANY WARRANTIES WHATSOEVER
- THE USER ASSUMES ALL RISKS ASSOCIATED WITH THE USE OF THIS SOFTWARE
- THE USER IS SOLELY RESPONSIBLE FOR BACKING UP ALL DATA BEFORE USING THE SOFTWARE
- THE USER IS SOLELY RESPONSIBLE FOR VERIFYING ALL ACTIONS PERFORMED BY THE SOFTWARE
- THE USER BEARS FULL RESPONSIBILITY FOR ANY CONSEQUENCES ARISING FROM THE USE OF THIS SOFTWARE

#### 3. NO WARRANTIES

TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW, THE AUTHOR EXPRESSLY DISCLAIMS ALL WARRANTIES, WHETHER EXPRESS, IMPLIED, STATUTORY, OR OTHERWISE, INCLUDING BUT NOT LIMITED TO:

- WARRANTIES OF MERCHANTABILITY
- WARRANTIES OF FITNESS FOR A PARTICULAR PURPOSE
- WARRANTIES OF TITLE OR NON-INFRINGEMENT
- WARRANTIES OF ACCURACY, RELIABILITY, OR COMPLETENESS
- WARRANTIES OF UNINTERRUPTED OR ERROR-FREE OPERATION

---

## 🚧 DEVELOPMENT STATUS

### ALPHA SOFTWARE NOTICE

**THIS SOFTWARE IS IN ACTIVE DEVELOPMENT AND IS PROVIDED "AS IS" WITHOUT ANY WARRANTIES WHATSOEVER.**

#### 1. DEVELOPMENT STAGE

THE USER ACKNOWLEDGES AND ACCEPTS THAT:

- THIS SOFTWARE IS CURRENTLY IN **ALPHA DEVELOPMENT STAGE**
- THE SOFTWARE IS NOT YET FEATURE-COMPLETE OR STABLE
- THE SOFTWARE IS SUBJECT TO SIGNIFICANT CHANGES WITHOUT NOTICE
- THE SOFTWARE MAY CONTAIN BUGS, ERRORS, OR DEFICIENCIES
- THE SOFTWARE MAY NOT FUNCTION AS INTENDED OR DOCUMENTED
- THE SOFTWARE MAY NOT BE SUITABLE FOR PRODUCTION USE

#### 2. UNPREDICTABLE BEHAVIOR

THE USER UNDERSTANDS THAT THE SOFTWARE MAY EXHIBIT UNPREDICTABLE BEHAVIOR INCLUDING BUT NOT LIMITED TO:

- CRASHES OR FREEZES DURING OPERATION
- INCORRECT IDENTIFICATION OF DUPLICATE FILES
- FAILURE TO DETECT ACTUAL DUPLICATES
- ACCIDENTAL SELECTION OF INCORRECT FILES
- UNINTENDED MOVEMENT OR DELETION OF FILES
- DATA CORRUPTION OR LOSS
- PERFORMANCE DEGRADATION OR HANGS
- INCOMPATIBILITY WITH CERTAIN SYSTEMS OR CONFIGURATIONS
- INCORRECT FILE HASH COMPUTATION
- FAILURE TO PROPERLY HANDLE LARGE NUMBERS OF FILES

#### 3. RECOMMENDATIONS

THE USER IS STRONGLY ADVISED TO:

- USE THE SOFTWARE ONLY FOR TESTING AND EVALUATION PURPOSES
- NEVER USE THE SOFTWARE WITH CRITICAL OR IRREPLACEABLE DATA
- ALWAYS MAINTAIN COMPLETE AND VERIFIED BACKUPS
- TEST THE SOFTWARE THOROUGHLY IN A SAFE ENVIRONMENT FIRST
- VERIFY ALL ACTIONS AND SELECTIONS BEFORE EXECUTING THEM
- REPORT ANY ISSUES OR UNEXPECTED BEHAVIOR TO THE AUTHOR
- READ THE DOCUMENTATION CAREFULLY BEFORE USE

---

<div align="center">

**⭐ Star this repo if you find it useful!**

</div>