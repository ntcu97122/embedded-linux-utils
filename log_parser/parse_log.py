#!/usr/bin/env python3

import sys
import re

LOG_FILE = "/var/log/syslog"

def parse_log(file_path):
    error_keywords = ['error', 'fail', 'warning', 'critical']
    with open(file_path, 'r', errors='ignore') as f:
        for line in f:
            if any(word in line.lower() for word in error_keywords):
                print(line.strip())

if __name__ == "__main__":
    log_file = sys.argv[1] if len(sys.argv) > 1 else LOG_FILE
    print(f"正在掃描：{log_file}")
    parse_log(log_file)
