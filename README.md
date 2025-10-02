# GitHub Repositories Backup Tools <sup>v0.9.3</sup>

![GitHub top language](https://img.shields.io/github/languages/top/smartlegionlab/github-repos-backup-tools)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/smartlegionlab/github-repos-backup-tools)](https://github.com/smartlegionlab/github-repos-backup-tools/)
[![GitHub](https://img.shields.io/github/license/smartlegionlab/github-repos-backup-tools)](https://github.com/smartlegionlab/github-repos-backup-tools/blob/master/LICENSE)

> Professional solution for automatic cloning and backup of GitHub repositories and gists with enhanced reliability

---

## 🔥 Key Features

- **Complete Backup** - Clone both public and private repositories/gists
- **Smart Update System** - Existing clones are updated via `git pull`
- **Resilient Retry Mechanism** - 5 automatic retries for failed operations
- **Archive Support** - Create compressed ZIP archives
- **System Control** - Option to shutdown/reboot after completion
- **Real-time Monitoring** - Improved progress bar with statistics
- **Cross-platform** - Works on Linux and Termux (Android)
- **Configurable Timeout** - Set custom timeout for Git operations (`--timeout N`)
- **Security** - Path traversal attack protection
- **Error Reporting** - Detailed failure reports with retry status

## 🚨 Important Notice

- Added new --reboot flag that performs system reboot after completion
- Made --reboot and --shutdown mutually exclusive using argparse group
- Added reboot() method similar to shutdown() but for system restart
- Changed the priority of receiving and checking information when initializing the application
- Fixed incorrect display of some user interface elements


## 🖥 System Requirements

- Python 3.8+
- Git 2.20+
- SSH client (for authentication)
- 100MB+ free disk space (varies by repository size)


## 🚀 Quick Start Guide

### 1. Installation
```bash
git clone https://github.com/smartlegionlab/github-repos-backup-tools.git
cd github-repos-backup-tools
```

### 2. Configuration
Create `.config.ini` file:
```ini
[github]
token = your_github_token_here
```

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

## 💻 Usage Options

| Command       | Description                              |
|---------------|------------------------------------------|
| `-r`          | Clone all repositories                   |
| `-g`          | Clone all gists                          |
| `--archive`   | Create compressed backup archive         |
| `--verbose`   | Show detailed debug output               |
| `--shutdown`  | Shutdown computer after completion       |
| `--reboot`    | Restart computer after completion        |
| `--timeout N` | Set timeout for Git operations (seconds) |

**Common Command Combinations:**
```bash
# Basic backup
python app.py -r -g

# Backup with archive creation
python app.py -r --archive

# Full backup with shutdown
python app.py -r -g --shutdown

# Full backup with reboot
python app.py -r -g --reboot

# Debug mode
python app.py -g --verbose
```

## 📂 File Structure
Backups are organized in your home directory:
```
~/
└── [username]_github_backup/
    ├── repositories/  # All cloned repositories
    ├── gists/        # All cloned gists
 [username]_github_backup.zip    # Created when using --archive
```

## 🔧 Technical Details

- **Retry Logic**: 5 attempts for each clone/update operation
- **Timeout**: 30 seconds per git operation
- **Error Handling**: Automatic cleanup of failed clones
- **Progress Tracking**: Real-time visual feedback
- **System Integration**: Supports shutdown/reboot commands
- **Timeout**: Configurable per operation (default: 20s)
- **Security**: Strict path validation to prevent directory traversal
- **Error Handling**: Clean failure tracking with itemized reports

## ❓ Frequently Asked Questions

**Q: How to cancel scheduled shutdown?**  
A: Use `shutdown -c` (Linux) or `shutdown /a` (Windows)

**Q: Where are backups stored?**  
A: In `~/[your_username]_github_backup/`

**Q: How to update existing clones?**  
A: Just run the tool again - it automatically does `git pull`

## 📝 Changelog

**v0.9.3 Updates:**
- Implemented configurable operation timeout (`--timeout`)
- Added path sanitization and validation
- Fixed f-string formatting in backup reports 
- Improved UI element rendering stability
- Added forced directory structure enforcement

---

**Author**: A.A. Suvorov  
**License**: [BSD 3-Clause "New" or "Revised" License](https://github.com/smartlegionlab/github-repos-backup-tools/blob/master/LICENSE)  
**Support**: Open issue on [GitHub](https://github.com/smartlegionlab/github-repos-backup-tools/issues)

**Example output without using the `--verbose` flag:**

`python app.py -r -g`

```
************************************************************************************************************************
------------------------------------------- Github Repositories Backup Tools -------------------------------------------
------------------------------------------------------------------------------------------------------------------------

Getting a token from a .config.ini file: ✅

Checking the token for validity:
Token is valid: ✅

Getting user login:
✅ Login: login

Parsing arguments:

Clone repositories: ✅
Clone gists: ✅
Make archive: ⚠
Shutdown: ⚠
Reboot: ✅
Verbose: ⚠

Forming a path to the directory:
✅ Path: /home/user/login_github_backup

------------------------------------------------------------------------------------------------------------------------
------------------------------------------------ Cloning repositories:  ------------------------------------------------
------------------------------------------------------------------------------------------------------------------------

Target directory: /home/user/login_github_backup/repositories
------------------------------------------------------------------------------------------------------------------------
Getting repositories:

-------------------------
✅ Found 248 repositories.
-------------------------

[################################################--] 97.98% | 243/248 | Failed: 9 | Cloning: repo243

```

**Example output when using the `--verbose` flag:**

`python app -r -g --verbose`

```
************************************************************************************************************************
------------------------------------------- Github Repositories Backup Tools -------------------------------------------
------------------------------------------------------------------------------------------------------------------------

Getting a token from a .config.ini file: ✅

Checking the token for validity:
Token is valid: ✅

Getting user login:
✅ Login: login

Parsing arguments:

Clone repositories: ✅
Clone gists: ✅
Make archive: ⚠
Shutdown: ⚠
Reboot: ✅
Verbose: ✅

Forming a path to the directory:
✅ Path: /home/user/login_github_backup

------------------------------------------------------------------------------------------------------------------------
------------------------------------------------ Cloning repositories:  ------------------------------------------------
------------------------------------------------------------------------------------------------------------------------

Target directory: /home/user/login_github_backup/repositories
------------------------------------------------------------------------------------------------------------------------
Getting repositories:

-------------------------
✅ Found 3 repositories.
-------------------------

---------------------------------------
1/3/0: Cloning: login/repo1
---------------------------------------
✅ Repository updated successfully: 
/home/user/login_github_backup/repositories/login/repo1
------------------------------------------------
2/3/0: Cloning: login/repo2
------------------------------------------------
⚠ Pull operation timed out: 
/home/user/login_github_backup/repositories/login/repo2
⚠ Pull failed. Removing and re-cloning: 
/home/user/login_github_backup/repositories/login/repo2
⚠ Clone operation timed out: 
/home/user/login_github_backup/repositories/login/repo2
⚠ Removing incomplete repositories: 
/home/user/login_github_backup/repositories/login/repo2
---------------------------------------------------------------
3/3/1: Cloning: login/repo3
---------------------------------------------------------------
⚠ Pull operation timed out: 
/home/user/login_github_backup/repositories/login/repo3
⚠ Pull failed. Removing and re-cloning: 
/home/user/login_github_backup/repositories/login/repo3
✅ Repository cloned successfully: 
/home/user/login_github_backup/repositories/login/repo3
------------------------------------------------------------------------------------------------------------------------

-----------------------------------------
Retrying failed repositories: 1 remaining
-----------------------------------------

------------------------------------------------------------
1/1/1: Retrying: login/repo2
------------------------------------------------------------
✅ Repository cloned successfully: 
/home/user/login_github_backup/repositories/login/repo2

------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------- Cloning gists:  ----------------------------------------------------
------------------------------------------------------------------------------------------------------------------------

Target directory: /home/user/login_github_backup/gists
------------------------------------------------------------------------------------------------------------------------
Getting gists:

------------------
✅ Found 3 gists.
------------------

--------------------------------------------------
1/3/0: Cloning: name1
--------------------------------------------------
✅ Repository updated successfully: 
/home/user/login_github_backup/gists/name1
--------------------------------------------------
2/3/0: Cloning: name2
--------------------------------------------------
⚠ Pull operation timed out: 
/home/user/login_github_backup/gists/name2
⚠ Pull failed. Removing and re-cloning: 
/home/user/login_github_backup/gists/name2
⚠ Clone operation timed out: 
/home/user/login_github_backup/gists/name2
⚠ Removing incomplete gists: 
/home/user/login_github_backup/gists/name2
--------------------------------------------------
3/3/1: Cloning: name3
--------------------------------------------------
⚠ Pull operation timed out: 
/home/user/login_github_backup/gists/name3
⚠ Pull failed. Removing and re-cloning: 
/home/user/login_github_backup/gists/name3
✅ Repository cloned successfully: 
/home/user/login_github_backup/gists/name3
------------------------------------------------------------------------------------------------------------------------

----------------------------------
Retrying failed gists: 1 remaining
----------------------------------

------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------
1/1/1: Retrying: name2
-------------------------------------------------
✅ Repository cloned successfully: 
/home/user/login_github_backup/gists/name2
------------------------------------------------------------------------------------------------------------------------
------------------------------------------ https://github.com/smartlegionlab/ ------------------------------------------
------------------------------------------ Copyright © 2025, Alexander Suvorov -----------------------------------------
************************************************************************************************************************
```

***

## Disclaimer of liability:

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
    AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
    IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
    FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
    DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
    SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
    CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
    OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
    OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

***

## License
    
    Licensed under the terms of the BSD 3-Clause License
    (see LICENSE for details).
    Copyright © 2025, Alexander Suvorov
    All rights reserved.
