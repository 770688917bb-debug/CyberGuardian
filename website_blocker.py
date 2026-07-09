#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🔥 WEBSITE BLOCKER - PYTHON EDITION 🔥
[ EXTREMELY TERRIFYING & POWERFUL ]
"""

import os
import sys
import subprocess
import argparse
from datetime import datetime
from pathlib import Path

# 💀 COLORS OF DOOM 💀
class Colors:
    RED = '\033[0;31m'
    BRIGHT_RED = '\033[1;31m'
    BLACK = '\033[0;30m'
    WHITE = '\033[1;37m'
    DARK_RED = '\033[0;91m'
    YELLOW = '\033[1;33m'
    CYAN = '\033[0;36m'
    MAGENTA = '\033[0;35m'
    RESET = '\033[0m'

class WebsiteBlocker:
    VERSION = "6.66"
    
    def __init__(self):
        self.hosts_file = "/system/etc/hosts"
        self.backup_dir = Path.home() / ".blocker_backups"
        self.blocked_list = Path.home() / ".blocked_websites"
        self.log_file = Path.home() / ".blocker_log"
        self.setup_directories()
    
    def setup_directories(self):
        """Setup required directories"""
        self.backup_dir.mkdir(exist_ok=True)
        self.blocked_list.touch(exist_ok=True)
        self.log_file.touch(exist_ok=True)
    
    @staticmethod
    def print_skull_header():
        """Print terrifying header"""
        os.system('clear')
        print(f"{Colors.BRIGHT_RED}")
        print("""
    ██╗    ██╗███████╗██████╗ ███████╗██╗████████╗███████╗
    ██║    ██║██╔════╝██╔══██╗██╔════╝██║╚══██╔══╝██╔════╝
    ██║ █╗ ██║█████╗  ██████╔╝███████╗██║   ██║   █████╗  
    ██║███╗██║██╔══╝  ██╔══██╗╚════██║██║   ██║   ██╔══╝  
    ╚███╔███╔╝███████╗██████╔╝███████║██║   ██║   ███████╗
     ╚══╝╚══╝ ╚══════╝╚═════╝ ╚══════╝╚═╝   ╚═╝   ╚══════╝
                                                       
    ╔═══════════════════════════════════════════════════════╗
    ║      🔥 EXTREME WEBSITE BLOCKER v6.66 🔥             ║
    ║           [ TOTAL ANNIHILATION MODE ]                ║
    ║         ⚠️  WARNING: EXTREMELY TERRIFYING ⚠️          ║
    ╚═══════════════════════════════════════════════════════╝
        """)
        print(f"{Colors.RESET}\n")
    
    @staticmethod
    def terror_success(msg):
        print(f"{Colors.BRIGHT_RED}[💀 BLOCKED]{Colors.RESET} {msg}")
    
    @staticmethod
    def terror_error(msg):
        print(f"{Colors.RED}[☠️  ERROR]{Colors.RESET} {msg}")
    
    @staticmethod
    def terror_info(msg):
        print(f"{Colors.CYAN}[⚡ INFO]{Colors.RESET} {msg}")
    
    @staticmethod
    def terror_warning(msg):
        print(f"{Colors.YELLOW}[⚠️  WARNING]{Colors.RESET} {msg}")
    
    @staticmethod
    def skull_separator():
        print(f"{Colors.BRIGHT_RED}════════════════════════════════════════════════════════{Colors.RESET}")
    
    @staticmethod
    def extract_domain(url):
        """Extract domain from URL"""
        url = url.replace("http://", "").replace("https://", "")
        url = url.replace("www.", "")
        url = url.split('/')[0].split(':')[0]
        return url
    
    def check_root(self):
        """Check if running as root"""
        if os.geteuid() != 0:
            self.terror_error("This tool requires ROOT privileges (use: sudo or su)")
            sys.exit(1)
    
    def block_website(self, url):
        """Block a website"""
        domain = self.extract_domain(url)
        
        if not domain:
            self.terror_error(f"Invalid URL: {url}")
            return False
        
        # Check if already blocked
        if self.blocked_list.exists():
            with open(self.blocked_list, 'r') as f:
                if domain in f.read():
                    self.terror_warning(f"Website already blocked: {domain}")
                    return False
        
        print(f"\n{Colors.BRIGHT_RED}🔥 BLOCKING: {domain} 🔥{Colors.RESET}")
        
        try:
            # Add to hosts file
            with open(self.hosts_file, 'a') as f:
                f.write(f"127.0.0.1 {domain}\n")
                f.write(f"0.0.0.0 {domain}\n")
                f.write(f"127.0.0.1 www.{domain}\n")
                f.write(f"0.0.0.0 www.{domain}\n")
        except PermissionError:
            self.terror_warning("Cannot write to hosts file (permission denied)")
        
        # Add to blocked list
        with open(self.blocked_list, 'a') as f:
            f.write(f"{domain}\n")
        
        # Log activity
        with open(self.log_file, 'a') as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] BLOCKED: {domain}\n")
        
        self.terror_success(f"Website PERMANENTLY BLOCKED: {domain}")
        print(f"{Colors.BRIGHT_RED}⚠️  This website is now INACCESSIBLE ⚠️{Colors.RESET}\n")
        return True
    
    def unblock_website(self, url):
        """Unblock a website"""
        domain = self.extract_domain(url)
        
        if not domain:
            self.terror_error(f"Invalid URL: {url}")
            return False
        
        if not self.blocked_list.exists() or domain not in self.blocked_list.read_text():
            self.terror_warning(f"Website is not blocked: {domain}")
            return False
        
        print(f"\n{Colors.BRIGHT_RED}🔓 UNBLOCKING: {domain} 🔓{Colors.RESET}")
        
        try:
            # Remove from hosts file
            with open(self.hosts_file, 'r') as f:
                lines = f.readlines()
            
            with open(self.hosts_file, 'w') as f:
                for line in lines:
                    if domain not in line:
                        f.write(line)
        except PermissionError:
            self.terror_warning("Cannot write to hosts file (permission denied)")
        
        # Remove from blocked list
        with open(self.blocked_list, 'r') as f:
            lines = f.readlines()
        
        with open(self.blocked_list, 'w') as f:
            for line in lines:
                if domain not in line:
                    f.write(line)
        
        # Log activity
        with open(self.log_file, 'a') as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] UNBLOCKED: {domain}\n")
        
        self.terror_success(f"Website UNBLOCKED: {domain}")
        return True
    
    def list_blocked_websites(self):
        """List all blocked websites"""
        self.skull_separator()
        print(f"{Colors.BRIGHT_RED}[⚰️  BLOCKED WEBSITES GRAVEYARD ⚰️]{Colors.RESET}\n")
        
        if not self.blocked_list.exists() or self.blocked_list.stat().st_size == 0:
            self.terror_info("No websites are blocked yet")
        else:
            with open(self.blocked_list, 'r') as f:
                domains = f.readlines()
            
            for i, domain in enumerate(domains, 1):
                domain = domain.strip()
                print(f"  {Colors.RED}{i}. ☠️  {domain}{Colors.RESET}")
        
        self.skull_separator()
    
    def show_activity_log(self):
        """Show activity log"""
        self.skull_separator()
        print(f"{Colors.BRIGHT_RED}[📜 ACTIVITY LOG 📜]{Colors.RESET}\n")
        
        if not self.log_file.exists() or self.log_file.stat().st_size == 0:
            self.terror_info("No activity recorded")
        else:
            with open(self.log_file, 'r') as f:
                lines = f.readlines()
            
            for line in lines[-20:]:
                print(f"  {Colors.CYAN}{line.strip()}{Colors.RESET}")
        
        self.skull_separator()
    
    def show_menu(self):
        """Show interactive menu"""
        print(f"{Colors.BRIGHT_RED}")
        print("""
╔═══════════════════════════════════════════════════════╗
║           🔥 MAIN MENU - CHOOSE YOUR FATE 🔥          ║
╠═══════════════════════════════════════════════════════╣
║ 1. 💀 Block a website                                 ║
║ 2. 🔓 Unblock a website                               ║
║ 3. ⚰️  View all blocked websites                       ║
║ 4. 📜 View activity log                               ║
║ 5. 🔥 NUCLEAR OPTION - Block multiple websites        ║
║ 6. 💀 Exit (if you can...)                            ║
╚═══════════════════════════════════════════════════════╝
        """)
        print(f"{Colors.RESET}")
    
    def interactive_mode(self):
        """Interactive mode"""
        self.check_root()
        
        while True:
            self.show_menu()
            choice = input("Enter your choice [1-6]: ").strip()
            
            if choice == '1':
                url = input("\nEnter website URL to block: ").strip()
                if url:
                    self.block_website(url)
            elif choice == '2':
                url = input("\nEnter website URL to unblock: ").strip()
                if url:
                    self.unblock_website(url)
            elif choice == '3':
                self.list_blocked_websites()
            elif choice == '4':
                self.show_activity_log()
            elif choice == '5':
                print(f"\n{Colors.YELLOW}🔥 ENTERING NUCLEAR MODE - MASS DESTRUCTION 🔥{Colors.RESET}")
                print(f"{Colors.BRIGHT_RED}Enter website URLs (one per line, type 'DONE' when finished):{Colors.RESET}\n")
                while True:
                    url = input("URL: ").strip()
                    if url.upper() == 'DONE':
                        break
                    if url:
                        self.block_website(url)
            elif choice == '6':
                print(f"\n{Colors.BRIGHT_RED}🔥 Exiting the Blocker of Doom... 🔥{Colors.RESET}")
                sys.exit(0)
            else:
                self.terror_error("Invalid choice! Try again...")
            
            input("\nPress Enter to continue...")
            self.print_skull_header()

def main():
    blocker = WebsiteBlocker()
    blocker.print_skull_header()
    
    parser = argparse.ArgumentParser(
        description='🔥 Website Blocker - Terrifying Edition 🔥',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:
  sudo python3 website_blocker.py -b https://example.com
  sudo python3 website_blocker.py -u https://example.com
  sudo python3 website_blocker.py -l
  sudo python3 website_blocker.py              (interactive mode)
        """
    )
    
    parser.add_argument('-b', '--block', help='Block a website', type=str)
    parser.add_argument('-u', '--unblock', help='Unblock a website', type=str)
    parser.add_argument('-l', '--list', help='List all blocked websites', action='store_true')
    parser.add_argument('-v', '--version', help='Show version', action='version', version=f'v{WebsiteBlocker.VERSION}')
    
    args = parser.parse_args()
    
    if args.block:
        blocker.check_root()
        blocker.block_website(args.block)
    elif args.unblock:
        blocker.check_root()
        blocker.unblock_website(args.unblock)
    elif args.list:
        blocker.list_blocked_websites()
    else:
        blocker.interactive_mode()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.BRIGHT_RED}🔥 Emergency shutdown! 🔥{Colors.RESET}")
        sys.exit(0)
