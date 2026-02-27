# GitHub Repositories Backup Tools <sup>v1.3.0</sup>

A professional solution for automatic cloning and backup of all your GitHub repositories.

---

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/smartlegionlab/github-repos-backup-tools)](https://github.com/smartlegionlab/github-repos-backup-tools/releases)
![GitHub top language](https://img.shields.io/github/languages/top/smartlegionlab/github-repos-backup-tools)
[![GitHub](https://img.shields.io/github/license/smartlegionlab/github-repos-backup-tools)](https://github.com/smartlegionlab/github-repos-backup-tools/blob/master/LICENSE)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![Platform](https://img.shields.io/badge/platform-windows%20%7C%20linux%20%7C%20macos-lightgrey)
![GitHub last commit](https://img.shields.io/github/last-commit/smartlegionlab/github-repos-backup-tools)

---

## 🚀 Features

- **Full Backup** - clones ALL repositories (public and private) from your account
- **All Branches** - automatically saves ALL branches, not just default
- **Smart Update** - updates only repositories with changes in the last 5 minutes
- **Automatic Retries** - up to 5 attempts with exponential backoff on failures
- **Health Check** - automatic integrity verification of each repository
- **No SSH Required** - uses only HTTPS with token authentication
- **Token Persistence** - token is saved after first use and reused on subsequent runs
- **Progress with Error Counter** - visual progress bar showing error count
- **Detailed Report** - statistics on cloned, updated, skipped, and failed repositories
- **Archiving** - creates timestamped ZIP archive in the application folder
- **Power Management** - shutdown/reboot after completion (optional)

## 📁 Project Structure

```
~/github_backup_repos_tools/              # Main application folder
└── user/                                 # Your GitHub username
    ├── repositories/                     # All cloned repositories
    │   ├── repo1/                        # Full copy with ALL branches
    │   ├── repo2/
    │   └── ...
    └── config.json                       # Token file (automatically created)
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

### Power Management
| Command | Description |
|---------|-------------|
| `--shutdown` | Shutdown computer after completion |
| `--reboot` | Reboot computer after completion |

### Usage Examples
```bash
# Basic backup of all repositories
python app.py -r

# Backup without creating archive
python app.py -r --no-archive

# With increased timeout
python app.py -r --timeout 60

# Update token
python app.py -t

# Backup with shutdown after completion
python app.py -r --shutdown
```

## 📊 Example Output

```

```

## 🔄 How It Works

1. **Network Check** - verifies internet and GitHub API availability
2. **Authentication** - uses saved token or requests a new one
3. **Scanning** - gets list of all repositories (yours + from organizations)
4. **Clone/Update**:
   - If repository doesn't exist - clones with all branches
   - If exists - checks last commit date
   - Updates only if changes are older than 5 minutes
5. **Health Check** - verifies repository integrity after each operation
6. **Retries** - up to 5 attempts with exponential backoff on failures
7. **Report** - shows detailed statistics
8. **Archiving** - creates ZIP archive (if not disabled)

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

## 📌 What's New in v1.3.0

- ✅ New folder structure `~/github_backup_repos_tools/[username]/repositories/`
- ✅ Clones ALL branches, not just default
- ✅ Removed SSH dependency (HTTPS only)
- ✅ Detailed report with cloned/updated/skipped/failed breakdown

---

**Author**: Alexander Suvorov  
**License**: [BSD 3-Clause License](https://github.com/smartlegionlab/github-repos-backup-tools/blob/master/LICENSE)  
**Support**: [GitHub Issues](https://github.com/smartlegionlab/github-repos-backup-tools/issues)  
**Source Code**: [https://github.com/smartlegionlab/](https://github.com/smartlegionlab/github-repos-backup-tools)

---

<div align="center">

**⭐ Star this repo if you find it useful!**

</div>