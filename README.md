# GitHub Repositories Backup Tools <sup>v1.0.2</sup>

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/smartlegionlab/github-repos-backup-tools)](https://github.com/smartlegionlab/github-repos-backup-tools/releases)
![GitHub top language](https://img.shields.io/github/languages/top/smartlegionlab/github-repos-backup-tools)
[![GitHub](https://img.shields.io/github/license/smartlegionlab/github-repos-backup-tools)](https://github.com/smartlegionlab/github-repos-backup-tools/blob/master/LICENSE)

> Professional modular solution for automatic cloning and backup of GitHub repositories and gists with step-by-step execution pipeline

---

## 🎯 What's New in v1.0.2

### 🏗️ Completely Rewritten Architecture
- **Modular Step-by-Step Pipeline** - Each operation is now an independent step
- **Enhanced Error Handling** - Graceful failure recovery at each stage
- **Context Management** - Shared data between steps with proper isolation
- **Extensible Design** - Easy to add new steps and functionality

### 🔧 New Step-Based System
1. **Arguments Parsing** - Command line interface with validation
2. **Configuration Setup** - Secure token management
3. **GitHub Authentication** - Token validation and user verification
4. **Directory Setup** - Organized backup structure
5. **Operations** - Smart cloning/updating with retry logic
6. **Verification** - Integrity checks for all backups
7. **Reporting** - Comprehensive backup summary
8. **Archiving** - Optional compression with timestamps
9. **System Actions** - Shutdown/reboot options

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
| Command | Description |
|---------|-------------|
| `-r` | Backup repositories |
| `-g` | Backup gists |
| `--archive` | Create compressed backup archive |
| `--verbose` | Detailed debug output |
| `--timeout N` | Git operation timeout (seconds) |

### Power Management
| Command | Description |
|---------|-------------|
| `--shutdown` | Shutdown after completion |
| `--reboot` | Restart after completion |

**Note**: `--shutdown` and `--reboot` are mutually exclusive.

### Common Usage Examples
```bash
# Basic repository backup
python app.py -r

# Complete backup (repos + gists)
python app.py -r -g

# Backup with archive creation
python app.py -r -g --archive

# Backup with system shutdown
python app.py -r -g --shutdown

# Backup with system reboot
python app.py -r -g --reboot

# Debug mode with custom timeout
python app.py -r --verbose --timeout 60
```

## 📂 Backup Structure

```
~/
├── [username]_github_backup/          # Main backup directory
│   ├── repositories/                  # All cloned repositories
│   └── gists/                         # All cloned gists
└── github_[username]_YYYY-MM-DD_HH_MM_SS.zip  # Auto-generated archive
```

## 🔧 Technical Architecture

### Step Pipeline
```python
ArgumentsStep() # CLI parsing
ConfigurationStep() # Token management
AuthenticationStep() # GitHub auth
DirectorySetupStep() # Folder structure
RepositoriesStep() # Repositories operations
GistsStep() # Gist operations
VerificationStep() # Integrity check
ReportStep() # Summary report
ArchiveStep() # Compression
SystemActionsStep() # Power management
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

## 📝 Changelog

### v1.0.2 Major Release
- **Complete architectural rewrite** with modular step system
- **Enhanced error handling** and recovery mechanisms  
- **Smart update detection** with 5-minute threshold
- **Improved security** with path validation and token storage
- **Secure token management** - automatic setup on first run with encrypted storage
- **Better user experience** with structured output and progress tracking
- **Mutually exclusive power options** (`--shutdown`/`--reboot`)
- **Comprehensive verification** and reporting system
- **Instant process termination** with single Ctrl+C

### v0.9.4 Features
- Stable release with basic backup functionality
- Archive creation support
- Basic retry mechanism
- Progress bar implementation

---

**⚠️ IMPORTANT NOTE**: If you experience any issues with v1.0.2, please report them in the [Issues section](https://github.com/smartlegionlab/github-repos-backup-tools/issues) and temporarily use the latest stable version v0.9.4 while we investigate.

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

## 🎨 Application Flow

```
********************************************************************************
----------------------- Github Repositories Backup Tools -----------------------
--------------------------------------------------------------------------------


==================================================
STEP 1: 🔧 Arguments Parsing
==================================================
🔧 Parsing command line arguments...
📋 Parsed arguments:
   Backup: 📦 Repositories, 📝 Gists
   Timeout: 30s
   Verbose: ❌ Disabled
   Power: ❌ No action
✅ Step 1 completed: 🔧 Arguments Parsing

==================================================
STEP 2: ⚙️ Configuration Setup
==================================================
🔧 Checking and setting up configuration directories and tokens...
📁 Configuration directory: /home/user_name/.config/github_repos_backup_tools
✅ Token found in configuration
✅ Token received successfully
✅ Step 2 completed: ⚙️ Configuration Setup

==================================================
STEP 3: 🔑 GitHub Authentication
==================================================
🔧 Authenticating with GitHub...
🔑 Validating GitHub token...
   🔄 Attempt 1/3 (timeout: 30s)... ✅ (0.5s)
✅ Authenticated as: github_user_name
✅ Step 3 completed: 🔑 GitHub Authentication

==================================================
STEP 4: 📁 Directory Setup
==================================================
🔧 Creating backup directory structure...
📁 Main backup directory: /home/user_name/github_user_name_github_backup
📂 Creating subdirectories:
   ✅ repositories/
   ✅ gists/
✅ Step 4 completed: 📁 Directory Setup

==================================================
STEP 5: 🔄 Repositories Operations
==================================================
🔧 Fetching and cloning/updating repositories...
📦 Fetching repositories...
   🔄 Attempt 1/3 (timeout: 30s)... ✅ (0.9s)
   🔄 Attempt 1/3 (timeout: 30s)... ✅ (1.0s)
   🔄 Attempt 1/3 (timeout: 30s)... ✅ (1.0s)
   🔄 Attempt 1/3 (timeout: 30s)... ✅ (0.5s)
✅ Found 100 repositories

📦 Processing 100 repositories...
[##########] 100.00% | 100/100 | Failed: 1 | Processing: github_user_name/webpa...
🔄 Retrying 1 failed repositories...

🔄 Retrying 1 failed repositories...
[##########] 100.00% | 1/1 | Failed: 0 | Retrying: github_user_name/github-ssh-...
✅ All repositories processed successfully after retry!

✅ All repositories processed successfully after retry
✅ Step 5 completed: 🔄 Repositories Operations

==================================================
STEP 6: 🔄 Gists Operations
==================================================
🔧 Fetching and cloning/updating gists...
📝 Fetching gists...
   🔄 Attempt 1/3 (timeout: 30s)... ✅ (0.5s)
   🔄 Attempt 1/3 (timeout: 30s)... ✅ (0.4s)
✅ Found 1 gists

📝 Processing 1 gists...
[##########] 100.00% | 1/1 | Failed: 0 | Processing: a2e7733c3ba32963b7c0985e...
✅ Cloning/updating gists completed successfully!

✅ Step 6 completed: 🔄 Gists Operations

==================================================
STEP 7: ✅ Verification
==================================================
🔧 Verifying that all repositories and gists are properly cloned/updated...
📊 Repositories verification:
   Total: 100
   Valid: 100
   Missing: 0
📊 Gists verification:
   Total: 1
   Valid: 1
   Missing: 0
✅ All items verified successfully!
✅ Step 7 completed: ✅ Verification

==================================================
STEP 8: 📊 Report
==================================================
🔧 Generating backup report...

============================================================
📊 BACKUP REPORT
============================================================

📦 REPOSITORIES:
   Total: 100
   ✅ Successful: 100
   ❌ Failed: 0
   🎉 All repositories processed successfully!

📝 GISTS:
   Total: 1
   ✅ Successful: 1
   ❌ Failed: 0
   🎉 All gists processed successfully!

💾 BACKUP LOCATION:
   /home/user_name/github_user_name_github_backup

🎉 SUCCESS: All backup operations completed successfully!
============================================================
✅ Step 8 completed: 📊 Report

==================================================
STEP 9: 🗄️ Archive Creation
==================================================
🔧 Creating backup archive...
⚠️ Archive creation not requested - skipping
✅ Step 9 completed: 🗄️ Archive Creation

==================================================
STEP 10: ⚡ System Actions
==================================================
🔧 Executing system actions (shutdown/reboot)...
⚠️ No system actions requested - skipping
✅ Step 10 completed: ⚡ System Actions
--------------------------------------------------------------------------------
---------------------- https://github.com/smartlegionlab/ ----------------------
--------------------- Copyright © 2025, Alexander Suvorov ----------------------
********************************************************************************

👋 Backup process finished

```