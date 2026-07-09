#!/bin/bash

################################################################################
# CyberGuardian - Network Scanner
# ماسح الشبكة - أداة فحص الشبكات والأجهزة
################################################################################

set -e

# الألوان
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# المتغيرات
SCRIPT_NAME="CyberGuardian Network Scanner"
VERSION="1.0.0"
OUTPUT_DIR="./scan_results"

################################################################################
# الدوال المساعدة
################################################################################

print_header() {
    echo -e "${BLUE}"
    echo "╔═════════════════════════════════════════════��══════════════╗"
    echo "║          $SCRIPT_NAME                    ║"
    echo "║                    v$VERSION                              ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

show_usage() {
    cat << EOF
الاستخدام: $0 [خيارات]

الخيارات:
    -h, --host HOST              فحص جهاز واحد
    -r, --range RANGE            فحص نطاق IP (مثال: 192.168.1.0/24)
    -p, --port PORT              فحص منفذ معين
    -o, --output FILE            حفظ النتائج في ملف
    -v, --verbose                وضع مفصل
    --help                        عرض هذه الرسالة
    --version                     عرض إصدار البرنامج

أمثلة:
    # فحص جهاز واحد
    $0 -h 192.168.1.1

    # فحص نطاق IP
    $0 -r 192.168.1.0/24

    # فحص مع حفظ النتائج
    $0 -h 192.168.1.1 -o results.txt

EOF
}

################################################################################
# فحص المتطلبات
################################################################################

check_requirements() {
    print_info "جاري فحص المتطلبات..."
    
    local missing=0
    
    # فحص nmap
    if ! command -v nmap &> /dev/null; then
        print_warning "nmap غير مثبت"
        missing=1
    else
        print_success "nmap موجود"
    fi
    
    # فحص netstat أو ss
    if ! command -v netstat &> /dev/null && ! command -v ss &> /dev/null; then
        print_warning "netstat/ss غير موجود"
        missing=1
    else
        print_success "netstat/ss موجود"
    fi
    
    if [ $missing -eq 1 ]; then
        print_warning "بعض المتطلبات مفقودة. قد لا تعمل جميع الميزات."
    else
        print_success "جميع المتطلبات موجودة"
    fi
}

################################################################################
# فحص الجهاز الواحد
################################################################################

scan_single_host() {
    local host=$1
    local output=$2
    
    print_info "جاري فحص الجهاز: $host"
    
    if nmap "$host" &>/dev/null; then
        print_success "الجهاز نشط: $host"
        
        print_info "جاري فحص المنافذ..."
        nmap -p- -T4 "$host" > "${output}_full_scan.txt" 2>/dev/null
        print_success "تم فحص جميع المنافذ"
        
        print_info "جاري كشف الخدمات..."
        nmap -sV "$host" > "${output}_services.txt" 2>/dev/null
        print_success "تم كشف الخدمات"
        
        # عرض النتائج
        echo ""
        print_info "نتائج الفحص:"
        echo "---"
        cat "${output}_full_scan.txt" | grep -E "open|closed|filtered" | head -20
        echo "---"
    else
        print_error "الجهاز غير متاح: $host"
        return 1
    fi
}

################################################################################
# فحص نطاق IP
################################################################################

scan_ip_range() {
    local range=$1
    local output=$2
    
    print_info "جاري فحص النطاق: $range"
    
    print_info "جاري اكتشاف الأجهزة النشطة..."
    nmap -sn "$range" -oG "${output}_hosts.txt" 2>/dev/null
    
    local active_hosts=$(grep "Up" "${output}_hosts.txt" | awk '{print $2}')
    local count=$(echo "$active_hosts" | wc -l)
    
    print_success "تم العثور على $count جهاز نشط"
    
    print_info "جاري فحص المنافذ لكل جهاز..."
    nmap -p 22,80,443,3306,5432,8080 "$range" -oN "${output}_ports.txt" 2>/dev/null
    
    print_success "اكتمل فحص النطاق"
    
    echo ""
    print_info "ملخص النتائج:"
    echo "---"
    cat "${output}_ports.txt" | grep -E "Nmap scan|Host is|open|closed" | head -30
    echo "---"
}

################################################################################
# فحص منفذ معين
################################################################################

scan_port() {
    local host=$1
    local port=$2
    local output=$3
    
    print_info "جاري فحص المنفذ $port على $host"
    
    nmap -p "$port" "$host" -sV -oN "${output}_port_${port}.txt" 2>/dev/null
    
    if grep -q "open" "${output}_port_${port}.txt"; then
        print_success "المنفذ $port مفتوح على $host"
    else
        print_info "المنفذ $port مغلق أو مصفى على $host"
    fi
}

################################################################################
# البرنامج الرئيسي
################################################################################

main() {
    print_header
    
    # إنشاء مجلد النتائج
    mkdir -p "$OUTPUT_DIR"
    
    # المتغيرات
    local host=""
    local range=""
    local port=""
    local output="${OUTPUT_DIR}/scan_$(date +%Y%m%d_%H%M%S)"
    local verbose=0
    
    # معالجة المعاملات
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--host)
                host="$2"
                shift 2
                ;;
            -r|--range)
                range="$2"
                shift 2
                ;;
            -p|--port)
                port="$2"
                shift 2
                ;;
            -o|--output)
                output="$2"
                shift 2
                ;;
            -v|--verbose)
                verbose=1
                shift
                ;;
            --help)
                show_usage
                exit 0
                ;;
            --version)
                echo "CyberGuardian Network Scanner v$VERSION"
                exit 0
                ;;
            *)
                print_error "خيار غير معروف: $1"
                show_usage
                exit 1
                ;;
        esac
    done
    
    # فحص المتطلبات
    check_requirements
    echo ""
    
    # تنفيذ الفحص
    if [ -n "$host" ]; then
        scan_single_host "$host" "$output"
        if [ -n "$port" ]; then
            echo ""
            scan_port "$host" "$port" "$output"
        fi
    elif [ -n "$range" ]; then
        scan_ip_range "$range" "$output"
    else
        print_error "يجب تحديد جهاز أو نطاق IP"
        echo ""
        show_usage
        exit 1
    fi
    
    print_success "تم الانتهاء من الفحص"
    print_info "النتائج مخزنة في: $output*"
}

# تشغيل البرنامج
main "$@"
