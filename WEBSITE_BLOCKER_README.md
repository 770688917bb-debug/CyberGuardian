# Website Blocker Tool

## 🔥 EXTREMELY TERRIFYING WEBSITE BLOCKER 🔥

This tool allows you to block websites on Termux/Linux with an extremely terrifying interface.

### Features:
- 💀 Block/Unblock websites instantly
- ⚰️ View all blocked websites  
- 📜 Activity logging
- 🔥 Bulk block multiple websites
- 🎭 Extremely scary interface
- 💾 Backup and restore functionality

### Requirements:
- Root privileges (sudo)
- Linux/Termux
- bash or python3

### Installation:

```bash
# Switch to the website-blocker branch
git checkout website-blocker

# Make script executable
chmod +x website_blocker.sh
```

### Usage:

#### Using Bash:
```bash
# Interactive mode
sudo ./website_blocker.sh

# Block a website
sudo ./website_blocker.sh -b https://example.com

# Unblock a website
sudo ./website_blocker.sh -u https://example.com

# List all blocked websites
sudo ./website_blocker.sh -l
```

#### Using Python:
```bash
# Interactive mode
sudo python3 website_blocker.py

# Block a website
sudo python3 website_blocker.py -b https://example.com

# Unblock a website
sudo python3 website_blocker.py -u https://example.com

# List all blocked websites
sudo python3 website_blocker.py -l
```

### Menu Options:
1. 💀 Block a website
2. 🔓 Unblock a website
3. ⚰️ View all blocked websites
4. 📜 View activity log
5. 🔥 NUCLEAR OPTION - Block multiple websites
6. 💀 Exit

### ⚠️ WARNING:
- Requires ROOT privileges
- Modifies system hosts file
- Blocked websites become completely inaccessible
- Use only for authorized testing

### How It Works:
The tool modifies the system's `/system/etc/hosts` file to redirect blocked domains to 127.0.0.1 (localhost).

### Features:
- Domain extraction from any URL format
- Automatic www. variants blocking
- Complete activity logging
- Backup and restore functionality
- Terrifying visual interface

---

**Use responsibly!** 🔥
