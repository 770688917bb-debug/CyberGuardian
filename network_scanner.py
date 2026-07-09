#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CyberGuardian - Network Scanner (Python Version)
ماسح الشبكة - نسخة Python
"""

import sys
import os
import argparse
import socket
import subprocess
from datetime import datetime
from colorama import Fore, Style, init

# تهيئة colorama
init(autoreset=True)

class Colors:
    """فئة للألوان"""
    SUCCESS = Fore.GREEN
    ERROR = Fore.RED
    WARNING = Fore.YELLOW
    INFO = Fore.BLUE
    RESET = Style.RESET_ALL

class NetworkScanner:
    """فئة ماسح الشبكة الرئيسية"""
    
    VERSION = "1.0.0"
    
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.output_dir = "./scan_results"
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.create_output_dir()
    
    def create_output_dir(self):
        """إنشاء مجلد النتائج"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    @staticmethod
    def print_header():
        """طباعة رأس البرنامج"""
        header = f"""
{Colors.INFO}╔════════════════════════════════════════════════════════════╗
║          CyberGuardian - Network Scanner                  ║
║                    v{NetworkScanner.VERSION}                              ║
╚════════════════════════════════════════════════════════════╝{Colors.RESET}
"""
        print(header)
    
    @staticmethod
    def print_success(message):
        """طباعة رسالة نجاح"""
        print(f"{Colors.SUCCESS}✓ {message}{Colors.RESET}")
    
    @staticmethod
    def print_error(message):
        """طباعة رسالة خطأ"""
        print(f"{Colors.ERROR}✗ {message}{Colors.RESET}")
    
    @staticmethod
    def print_info(message):
        """طباعة رسالة معلومات"""
        print(f"{Colors.INFO}ℹ {message}{Colors.RESET}")
    
    @staticmethod
    def print_warning(message):
        """طباعة رسالة تحذير"""
        print(f"{Colors.WARNING}⚠ {message}{Colors.RESET}")
    
    def check_requirements(self):
        """فحص المتطلبات"""
        self.print_info("جاري فحص المتطلبات...")
        
        requirements = {
            'nmap': 'nmap',
        }
        
        missing = []
        for tool, cmd in requirements.items():
            if subprocess.run(
                ['which', cmd],
                capture_output=True
            ).returncode != 0:
                self.print_warning(f"{tool} غير مثبت")
                missing.append(tool)
            else:
                self.print_success(f"{tool} موجود")
        
        if missing:
            self.print_warning(f"بعض المتطلبات مفقودة: {', '.join(missing)}")
        else:
            self.print_success("جميع المتطلبات موجودة")
    
    def scan_single_host(self, host):
        """فحص جهاز واحد"""
        self.print_info(f"جاري فحص الجهاز: {host}")
        
        # فحص الاتصال
        try:
            socket.gethostbyname(host)
            self.print_success(f"الجهاز متاح: {host}")
        except socket.gaierror:
            self.print_error(f"لا يمكن الوصول للجهاز: {host}")
            return False
        
        # فحص المنافذ الشهيرة
        common_ports = [21, 22, 80, 443, 3306, 5432, 8080, 8443]
        output_file = os.path.join(
            self.output_dir,
            f"scan_{self.timestamp}_{host.replace('.', '_')}.txt"
        )
        
        self.print_info(f"جاري فحص {len(common_ports)} منفذ شهير...")
        
        open_ports = []
        for port in common_ports:
            if self.is_port_open(host, port):
                open_ports.append(port)
                self.print_success(f"المنفذ {port} مفتوح")
        
        # حفظ النتائج
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"Network Scan Report - ماسح الشبكة\n")
            f.write(f"Host: {host}\n")
            f.write(f"Time: {datetime.now()}\n")
            f.write(f"{'='*50}\n\n")
            f.write(f"Open Ports: المنافذ المفتوحة\n")
            for port in open_ports:
                f.write(f"  - {port}\n")
        
        self.print_success(f"النتائج محفوظة في: {output_file}")
        return True
    
    def scan_ip_range(self, ip_range):
        """فحص نطاق IP"""
        self.print_info(f"جاري فحص النطاق: {ip_range}")
        
        output_file = os.path.join(
            self.output_dir,
            f"range_scan_{self.timestamp}.txt"
        )
        
        try:
            # استخدام nmap
            cmd = ['nmap', '-sn', ip_range, '-oG', '-']
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                self.print_success("اكتمل فحص النطاق")
                
                # حفظ النتائج
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(f"Range Scan Report - تقرير فحص النطاق\n")
                    f.write(f"Range: {ip_range}\n")
                    f.write(f"Time: {datetime.now()}\n")
                    f.write(f"{'='*50}\n\n")
                    f.write(result.stdout)
                
                self.print_success(f"النتائج محفوظة في: {output_file}")
            else:
                self.print_error("فشل فحص النطاق")
        
        except subprocess.TimeoutExpired:
            self.print_error("انتهت مهلة الفحص")
        except Exception as e:
            self.print_error(f"خطأ: {str(e)}")
    
    @staticmethod
    def is_port_open(host, port, timeout=1):
        """فحص ما إذا كان المنفذ مفتوح"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except Exception:
            return False
    
    def scan_port(self, host, port):
        """فحص منفذ معين"""
        self.print_info(f"جاري فحص المنفذ {port} على {host}")
        
        if self.is_port_open(host, port):
            self.print_success(f"المنفذ {port} مفتوح على {host}")
        else:
            self.print_info(f"المنفذ {port} مغلق أو مصفى على {host}")

def main():
    """البرنامج الرئيسي"""
    parser = argparse.ArgumentParser(
        description='CyberGuardian - Network Scanner',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
أمثلة:
  # فحص جهاز واحد
  python3 network_scanner.py -h 192.168.1.1
  
  # فحص نطاق IP
  python3 network_scanner.py -r 192.168.1.0/24
  
  # فحص منفذ معين
  python3 network_scanner.py -h 192.168.1.1 -p 80
        """
    )
    
    parser.add_argument(
        '-h', '--host',
        help='فحص جهاز واحد',
        type=str
    )
    parser.add_argument(
        '-r', '--range',
        help='فحص نطاق IP (مثال: 192.168.1.0/24)',
        type=str
    )
    parser.add_argument(
        '-p', '--port',
        help='فحص منفذ معين',
        type=int
    )
    parser.add_argument(
        '-v', '--verbose',
        help='وضع مفصل',
        action='store_true'
    )
    parser.add_argument(
        '--version',
        help='عرض إصدار البرنامج',
        action='version',
        version=f'CyberGuardian v{NetworkScanner.VERSION}'
    )
    
    args = parser.parse_args()
    
    # إنشاء الماسح
    scanner = NetworkScanner(verbose=args.verbose)
    scanner.print_header()
    
    # فحص المتطلبات
    scanner.check_requirements()
    print()
    
    # تنفيذ الفحص
    try:
        if args.host:
            scanner.scan_single_host(args.host)
            if args.port:
                print()
                scanner.scan_port(args.host, args.port)
        elif args.range:
            scanner.scan_ip_range(args.range)
        else:
            parser.print_help()
            sys.exit(1)
        
        scanner.print_success("تم الانتهاء من الفحص")
    
    except KeyboardInterrupt:
        print()
        scanner.print_warning("تم إيقاف البرنامج من قبل المستخدم")
        sys.exit(0)
    except Exception as e:
        scanner.print_error(f"خطأ: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
