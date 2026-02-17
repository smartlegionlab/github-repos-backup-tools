# GitHub Repositories Backup Tools <sup>v1.2.0</sup>

---

A professional, modular solution for automatically cloning and backing up GitHub repositories and GIST files.

---

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/smartlegionlab/github-repos-backup-tools)](https://github.com/smartlegionlab/github-repos-backup-tools/releases)
![GitHub top language](https://img.shields.io/github/languages/top/smartlegionlab/github-repos-backup-tools)
[![GitHub](https://img.shields.io/github/license/smartlegionlab/github-repos-backup-tools)](https://github.com/smartlegionlab/github-repos-backup-tools/blob/master/LICENSE)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![Platform](https://img.shields.io/badge/platform-windows%20%7C%20linux%20%7C%20macos%20%7C%20termux-lightgrey)
![GitHub last commit](https://img.shields.io/github/last-commit/smartlegionlab/github-repos-backup-tools)
![GitHub Stars](https://img.shields.io/github/stars/smartlegionlab/github-repos-backup-tools?style=social)

---

**WARNING!!!** - Вы можете использовать улучшенные версии данного приложения. Новая экоситема для клонирования, обновления, скачивания репозиториев:

**Smart Repository Manager**:

- [CORE](https://github.com/smartlegionlab/smart-repository-manager-core) - A Python library for managing Git repositories with intelligent synchronization, SSH configuration validation, and GitHub integration.
- [CLI](https://github.com/smartlegionlab/smart-repository-manager-cli) - A powerful desktop application for managing GitHub repositories with intelligent synchronization, SSH configuration, and comprehensive visual management tools.
- [GUI](https://github.com/smartlegionlab/smart-repository-manager-gui) - A comprehensive command-line tool for managing GitHub repositories with advanced synchronization, SSH configuration management, and intelligent local repository management.

---

## 🚀 Key Features

- **Complete Backup** - Clone both public and private repositories/gists
- **Smart Update System** - Only updates repositories with recent changes (5-minute threshold)
- **Resilient Retry Mechanism** - Automatic retries for failed operations
- **Archive Support** - Create timestamped compressed ZIP archives in home directory
- **System Control** - Option to shutdown/reboot after completion (mutually exclusive)
- **Real-time Monitoring** - Progress tracking with detailed statistics
- **Cross-platform** - Works on Windows, Linux, macOS and Termux (Android)
- **Configurable Timeout** - Set custom timeout for Git operations (`--timeout N`)
- **Security** - Path traversal attack protection and secure token storage
- **Detailed Reporting** - Comprehensive success/failure reports
- **Instant Process Termination** - Single Ctrl+C stops all operations immediately
- **Git Repository Health Checks** - Prevents broken clones with integrity validation
- **Git Health Verification** - Automatic detection and repair of broken repositories
- **Verbose Numbering** - Clear progress tracking with item counters in debug mode

## 🖥 System Requirements

- **Python**: 3.8+
- **Git**: 2.20+
- **SSH client** (for authentication)
- **Storage**: 100MB+ free space (varies by repository size)
- **Network**: Stable internet connection

## 🚀 Quick Start

### 1. Installation
```bash
git clone https://github.com/smartlegionlab/github-repos-backup-tools.git
cd github-repos-backup-tools
```

### 2. First Run (Automatic Token Setup)
```bash
python app.py -r -g
```
The application will guide you through token setup on first run.

### 3. Generate GitHub Token
1. Visit [GitHub Tokens](https://github.com/settings/tokens/new)
2. Select permissions:
   - ✅ `repo` (full repository access)
   - ✅ `gist` (gist access)
3. Generate and copy token

### 4. SSH Setup (Required)
```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Add to ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Add to GitHub account
cat ~/.ssh/id_ed25519.pub  # Copy this output
# Paste at https://github.com/settings/keys

# Verify connection
ssh -T git@github.com
```

## 💻 Usage

### Basic Commands
| Command        | Description |
|----------------|-------------|
| `-r`           | Backup repositories |
| `-g`           | Backup gists |
| `-t`           | Update token |
| `--no-archive` | Disable backup archive creation (archive is created by default |
| `--verbose`    | Detailed debug output |
| `--timeout N`  | Git operation timeout (seconds) |

### Power Management
| Command | Description |
|---------|-------------|
| `--shutdown` | Shutdown after completion |
| `--reboot` | Restart after completion |

**Note**: `--shutdown` and `--reboot` are mutually exclusive.

### Common Usage Examples
```bash
# Basic repository backup with archive creation
python app.py -r

# Complete backup (repos + gists) with archive creation
python app.py -r -g

# # Backup without creating an archive
python app.py -r -g --no-archive

# Backup with system shutdown with archive creation
python app.py -r -g --shutdown

# Backup with system reboot with archive creation
python app.py -r -g --reboot

# Debug mode with custom timeout with archive creation
python app.py -r --verbose --timeout 60

# Update token
python app.py -t
```

## 📂 Backup Structure

```
~/
├── [username]_github_backup/          # Main backup directory
│   ├── repositories/                  # All cloned repositories
│   └── gists/                         # All cloned gists
└── [username]_github_backup_YYYY-MM-DD_HH_MM_SS.zip  # Auto-generated archive
```

### Smart Update System
- Compares local commit dates with GitHub `pushed_at` timestamps
- 5-minute threshold to avoid unnecessary `git pull` operations
- Maintains data integrity while improving performance

### Security Features
- Secure token storage in user config directory
- Path traversal protection
- Input validation and sanitization
- Graceful error handling

## 📊 Performance Optimizations

- **Selective Updates**: Only updates repositories with changes >5 minutes old
- **Immediate Retries**: Failed operations automatically retried without delay
- **Progress Tracking**: Real-time feedback without verbose overhead
- **Memory Efficient**: Streamlined processing for large repository sets

## 🛠 Troubleshooting

### Common Issues

**Q: Authentication fails?**  
A: Verify token has `repo` and `gist` permissions and SSH key is properly set up. Use `--verbose` for details.

**Q: Clone operations timeout?**  
A: Increase timeout: `--timeout 60` for slower connections.

**Q: Where is my token stored?**  
A: In OS-specific config directory: `~/.config/github_repos_backup_tools/`

**Q: How to cancel scheduled shutdown?**  
A: Use `shutdown -c` (Linux/macOS) or `shutdown /a` (Windows)

**Q: SSH connection fails?**  
A: Verify SSH key is added to GitHub and test with `ssh -T git@github.com`

---

**Author**: Alexander Suvorov  
**License**: [BSD 3-Clause License](https://github.com/smartlegionlab/github-repos-backup-tools/blob/master/LICENSE)  
**Support**: [GitHub Issues](https://github.com/smartlegionlab/github-repos-backup-tools/issues)  
**Source**: [https://github.com/smartlegionlab/](https://github.com/smartlegionlab/)

## 🔒 Security Notice

This application:
- Stores tokens in user-specific config directories
- Validates all file paths to prevent directory traversal attacks  
- Uses minimal required permissions (repo, gist)
- Does not transmit data to third parties
- Provides clear audit trails of all operations

## 📄 License

```
Licensed under the terms of the BSD 3-Clause License
Copyright © 2025, Alexander Suvorov
All rights reserved.
```

## ⚠️ Disclaimer

THE SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND. Use at your own risk. The authors are not responsible for data loss, system instability, or any other issues arising from software use. Always test with non-critical data first.

**Legal Compliance**: Users are responsible for ensuring their use of this software complies with:
- GitHub's Terms of Service and API guidelines
- Local laws and regulations regarding data backup and access
- Copyright and intellectual property rights
- Any applicable export control laws

**Rate Limiting**: This tool uses GitHub's API - respect rate limits and avoid excessive requests that may impact GitHub's services.

**Data Responsibility**: You are solely responsible for the data you backup, including its security, storage, and legal compliance.

---

**📌 Development Status**: This application is currently in active development. While we strive for stability, some features may not work as expected. We appreciate your feedback and bug reports to help improve the software.

---

<div align="center">

**⭐ Star this repo if you find it useful!**

</div>

---

## OUTPUT

```text
********************************************************************************
----------------------- Github Repositories Backup Tools -----------------------
--------------------------------------------------------------------------------


🔧 Arguments Parsing: 
Parsing command line arguments...

Parsed arguments:
   Backup: Repositories, Gists, Archive
   Timeout: 30s
   Verbose: [x] Disabled
   Power: [x] No action

Configuration Setup: 
Checking and setting up configuration directories

Configuration directory: /home/user_name/.config/github_repos_backup_tools/github_token.json

Getting GitHub token: 

Token obtained successfully

GitHub Authentication: 
Authenticating with GitHub...
   Attempt 1/3 (timeout: 30s)... [ok] (0.5s)
[ok] Authenticated as: user_name

Directory Setup: 
Creating backup directory structure...
Main backup directory: /home/user_name/user_name_github_backup
   [ok] repositories/
   [ok] gists/

Repositories Operations: 
Fetching and cloning/updating repositories...
   Attempt 1/3 (timeout: 30s)... [ok] (2.0s)
   Attempt 1/3 (timeout: 30s)... [ok] (2.1s)
   Attempt 1/3 (timeout: 30s)... [ok] (2.1s)
   Attempt 1/3 (timeout: 30s)... [ok] (0.5s)
[ok] Found 100 repositories

Processing 100 repositories...
[##########] 100.00% | 100/100 | Failed: 0 | Processing: user_name/repo_name_...
[ok] Cloning/updating repositories completed successfully!


Gists Operations: 
Fetching and cloning/updating gists...
   Attempt 1/3 (timeout: 30s)... [ok] (0.5s)
   Attempt 1/3 (timeout: 30s)... [ok] (0.4s)
[ok] Found 1 gists

Processing 1 gists...
[##########] 100.00% | 1/1 | Failed: 0 | Processing: a2e7733c3ba32963b7c0985e...
[ok] Cloning/updating gists completed successfully!


[ok] Verification: 
Verifying that all repositories and gists are properly cloned/updated...
Repositories verification:
   Total: 100
   Valid: 100
   Missing: 0
Gists verification:
   Total: 1
   Valid: 1
   Missing: 0
[ok] All items verified successfully!

Report: 
Generating backup report...

REPOSITORIES:
   Total: 100
   [ok] Successful: 100
   [x] Failed: 0
   All repositories processed successfully!

GISTS:
   Total: 1
   [ok] Successful: 1
   [x] Failed: 0
   All gists processed successfully!

BACKUP LOCATION:
   /home/user_name/user_name_github_backup

[ok] SUCCESS: All backup operations completed successfully!
============================================================

Archive Creation: 
Creating backup archive...
[ok] Archive created successfully: /home/user_name/github_user_name_2025-11-19_18_11_46.zip
--------------------------------------------------------------------------------
---------------------- https://github.com/smartlegionlab/ ----------------------
--------------------- Copyright © 2025, Alexander Suvorov ----------------------
********************************************************************************
```
