#!/bin/bash

################################################################################
#                    🔥 WEBSITE BLOCKER - TERMUX EDITION 🔥
#                         [ EXTREMELY TERRIFYING ]
################################################################################

set -e

# 💀 COLORS OF DOOM 💀
RED='\033[0;31m'
BLACK='\033[0;30m'
WHITE='\033[1;37m'
DARK_RED='\033[0;91m'
BRIGHT_RED='\033[1;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

# ⚡ TERRIFYING VARIABLES ⚡
SCRIPT_NAME="WEBSITE BLOCKER"
VERSION="6.66"
HOSTS_FILE="/system/etc/hosts"
BACKUP_DIR="$HOME/.blocker_backups"
BLOCKED_LIST="$HOME/.blocked_websites"
LOG_FILE="$HOME/.blocker_log"

################################################################################
#                           👹 SKULL HEADER 👹
################################################################################

print_skull_header() {
    clear
    echo -e "${BRIGHT_RED}"
    cat << "EOF"
    
    ██╗    ██╗███████╗██████╗ ███████╗██╗████████╗███████╗
    ██║    ██║██╔════╝██╔══██╗██╔════╝██║╚══██╔══╝██╔════╝
    ██║ █╗ ██║█████╗  ██████╔╝███████╗██║   ██║   █████╗  
    ██║███╗██║██╔══╝  ██╔══██╗╚════██║██║   ██║   ██╔══╝  
    ╚███╔███╔╝███████╗██████╔╝███████║██║   ██║   ███████╗
     ╚══╝╚══╝ ╚══════╝╚═════╝ ╚══════╝╚═╝   ╚═╝   ╚══════╝
                                                           
    ╔═══════════════════════════════════════════════════════╗
    ║         🔥 EXTREME WEBSITE BLOCKER v${VERSION} 🔥         ║
    ║              [ TOTAL ANNIHILATION MODE ]             ║
    ║            ⚠️  WARNING: EXTREMELY TERRIFYING ⚠️       ║
    ╚═══════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}\n"
}

################################################################################
#                        💀 TERRIFYING MESSAGES 💀
################################################################################

terror_success() {
    echo -e "${BRIGHT_RED}[💀 BLOCKED]${NC} $1"
}

terror_error() {
    echo -e "${RED}[☠️  ERROR]${NC} $1"
}

terror_info() {
    echo -e "${CYAN}[⚡ INFO]${NC} $1"
}

terror_warning() {
    echo -e "${YELLOW}[⚠️  WARNING]${NC} $1"
}

skull_separator() {
    echo -e "${BRIGHT_RED}════════════════════════════════════════════════════════${NC}"
}

################################################################################
#                      🎭 SCARY ANIMATIONS 🎭
################################################################################

scary_animation() {
    local text="$1"
    echo -ne "${BRIGHT_RED}"
    for char in $(echo "$text" | fold -w1); do
        echo -n "$char"
        sleep 0.05
    done
    echo -e "${NC}"
}

loading_animation() {
    local frames=("⠋" "⠙" "⠹" "⠸" "⠼" "⠴" "⠦" "⠧" "⠇" "⠏")
    local text="$1"
    echo -ne "${BRIGHT_RED}${text} "
    for i in {1..20}; do
        echo -ne "\b${frames[$((i % 10))]}"
        sleep 0.1
    done
    echo -e "\b✓${NC}"
}

################################################################################
#                      🛡️ INITIALIZATION FUNCTIONS 🛡️
################################################################################

check_root() {
    if [[ $EUID -ne 0 ]]; then
        terror_error "This tool requires ROOT privileges (use: sudo or su)"
        exit 1
    fi
}

initialize_blocker() {
    mkdir -p "$BACKUP_DIR"
    touch "$BLOCKED_LIST"
    touch "$LOG_FILE"
    
    terror_info "Initializing Website Blocker..."
    loading_animation "Setting up directories"
}

################################################################################
#                    🔐 WEBSITE BLOCKING FUNCTIONS 🔐
################################################################################

extract_domain() {
    local url="$1"
    # Remove http:// or https://
    url="${url#http://}"
    url="${url#https://}"
    # Remove www.
    url="${url#www.}"
    # Get domain part
    echo "$url" | cut -d'/' -f1 | cut -d':' -f1
}

block_website() {
    local url="$1"
    local domain=$(extract_domain "$url")
    
    if [ -z "$domain" ]; then
        terror_error "Invalid URL: $url"
        return 1
    fi
    
    # Check if already blocked
    if grep -q "$domain" "$BLOCKED_LIST"; then
        terror_warning "Website already blocked: $domain"
        return 1
    fi
    
    scary_animation "🔥 BLOCKING: $domain 🔥"
    
    # Add to hosts file (if writable)
    if [ -w "$HOSTS_FILE" ]; then
        echo "127.0.0.1 $domain" >> "$HOSTS_FILE"
        echo "0.0.0.0 $domain" >> "$HOSTS_FILE"
        echo "127.0.0.1 www.$domain" >> "$HOSTS_FILE"
        echo "0.0.0.0 www.$domain" >> "$HOSTS_FILE"
    fi
    
    # Add to blocked list
    echo "$domain" >> "$BLOCKED_LIST"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] BLOCKED: $domain" >> "$LOG_FILE"
    
    terror_success "Website PERMANENTLY BLOCKED: $domain"
    echo -e "${BRIGHT_RED}⚠️  This website is now INACCESSIBLE ⚠️${NC}\n"
}

unblock_website() {
    local url="$1"
    local domain=$(extract_domain "$url")
    
    if [ -z "$domain" ]; then
        terror_error "Invalid URL: $url"
        return 1
    fi
    
    if ! grep -q "$domain" "$BLOCKED_LIST"; then
        terror_warning "Website is not blocked: $domain"
        return 1
    fi
    
    scary_animation "🔓 UNBLOCKING: $domain 🔓"
    
    # Remove from hosts file (if writable)
    if [ -w "$HOSTS_FILE" ]; then
        sed -i "/$domain/d" "$HOSTS_FILE"
        sed -i "/www\.$domain/d" "$HOSTS_FILE"
    fi
    
    # Remove from blocked list
    sed -i "/^$domain$/d" "$BLOCKED_LIST"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] UNBLOCKED: $domain" >> "$LOG_FILE"
    
    terror_success "Website UNBLOCKED: $domain"
}

list_blocked_websites() {
    skull_separator
    echo -e "${BRIGHT_RED}[⚰️  BLOCKED WEBSITES GRAVEYARD ⚰️]${NC}\n"
    
    if [ ! -s "$BLOCKED_LIST" ]; then
        terror_info "No websites are blocked yet"
    else
        local count=1
        while IFS= read -r domain; do
            echo -e "${RED}  $count. ☠️  $domain${NC}"
            ((count++))
        done < "$BLOCKED_LIST"
    fi
    
    skull_separator
}

show_activity_log() {
    skull_separator
    echo -e "${BRIGHT_RED}[📜 ACTIVITY LOG 📜]${NC}\n"
    
    if [ ! -s "$LOG_FILE" ]; then
        terror_info "No activity recorded"
    else
        tail -20 "$LOG_FILE" | while IFS= read -r line; do
            echo -e "${CYAN}  $line${NC}"
        done
    fi
    
    skull_separator
}

################################################################################
#                        🎯 MENU SYSTEM 🎯
################################################################################

show_menu() {
    echo -e "${BRIGHT_RED}"
    cat << "EOF"
╔═══════════════════════════════════════════════════════╗
║              🔥 MAIN MENU - CHOOSE YOUR FATE 🔥       ║
╠═══════════════════════════════════════════════════════╣
║ 1. 💀 Block a website                                 ║
║ 2. 🔓 Unblock a website                               ║
║ 3. ⚰️  View all blocked websites                       ║
║ 4. 📜 View activity log                               ║
║ 5. 🔥 NUCLEAR OPTION - Block multiple websites        ║
║ 6. 💾 Backup blocked list                             ║
║ 7. 📋 Restore from backup                             ║
║ 8. 💀 Exit (if you can...)                            ║
╚═══════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

bulk_block_websites() {
    terror_warning "🔥 ENTERING NUCLEAR MODE - MASS DESTRUCTION 🔥"
    echo -e "${BRIGHT_RED}Enter website URLs (one per line, type 'DONE' when finished):${NC}\n"
    
    while true; do
        read -p "URL: " url
        if [ "$url" = "DONE" ] || [ "$url" = "done" ]; then
            break
        fi
        if [ -n "$url" ]; then
            block_website "$url"
            echo ""
        fi
    done
}

backup_list() {
    local backup_file="$BACKUP_DIR/backup_$(date +%Y%m%d_%H%M%S).txt"
    cp "$BLOCKED_LIST" "$backup_file"
    terror_success "Backup created: $backup_file"
}

restore_backup() {
    if [ ! "$(ls -A "$BACKUP_DIR")" ]; then
        terror_error "No backups found"
        return 1
    fi
    
    echo -e "${BRIGHT_RED}Available backups:${NC}\n"
    ls -1 "$BACKUP_DIR" | nl
    
    read -p "Enter backup number: " backup_num
    local backup_file=$(ls -1 "$BACKUP_DIR" | sed -n "${backup_num}p")
    
    if [ -f "$BACKUP_DIR/$backup_file" ]; then
        cp "$BACKUP_DIR/$backup_file" "$BLOCKED_LIST"
        terror_success "Backup restored: $backup_file"
    else
        terror_error "Invalid backup number"
    fi
}

################################################################################
#                         🎮 MAIN LOOP 🎮
################################################################################

main() {
    print_skull_header
    
    # Check for root privileges
    check_root
    
    # Initialize
    initialize_blocker
    
    echo ""
    scary_animation "Welcome to the Website Blocker of DOOM!"
    echo ""
    
    while true; do
        show_menu
        read -p "Enter your choice [1-8]: " choice
        
        case $choice in
            1)
                echo ""
                read -p "Enter website URL to block: " url
                block_website "$url"
                ;;
            2)
                echo ""
                read -p "Enter website URL to unblock: " url
                unblock_website "$url"
                ;;
            3)
                echo ""
                list_blocked_websites
                ;;
            4)
                echo ""
                show_activity_log
                ;;
            5)
                echo ""
                bulk_block_websites
                ;;
            6)
                echo ""
                backup_list
                ;;
            7)
                echo ""
                restore_backup
                ;;
            8)
                scary_animation "🔥 Exiting the Blocker of Doom... 🔥"
                exit 0
                ;;
            *)
                terror_error "Invalid choice! Try again..."
                ;;
        esac
        
        echo ""
        read -p "Press Enter to continue..."
        clear
        print_skull_header
    done
}

# Display help
show_help() {
    cat << "EOF"
Usage: sudo ./website_blocker.sh [OPTION]

OPTIONS:
    -b, --block URL         Block a website
    -u, --unblock URL       Unblock a website
    -l, --list              Show all blocked websites
    -h, --help              Show this help message
    -v, --version           Show version

EXAMPLES:
    sudo ./website_blocker.sh -b https://example.com
    sudo ./website_blocker.sh -u https://example.com
    sudo ./website_blocker.sh -l
    sudo ./website_blocker.sh              (interactive mode)

EOF
}

# Command line arguments
if [[ $# -gt 0 ]]; then
    case "$1" in
        -b|--block)
            check_root
            initialize_blocker
            block_website "$2"
            ;;
        -u|--unblock)
            check_root
            initialize_blocker
            unblock_website "$2"
            ;;
        -l|--list)
            list_blocked_websites
            ;;
        -h|--help)
            show_help
            ;;
        -v|--version)
            echo "Website Blocker v$VERSION"
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
else
    main
fi
