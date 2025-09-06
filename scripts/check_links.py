import os
import re
import requests
import argparse
from urllib.parse import urlparse

def check_link(file_path, line_num, url):
    # Strip anchor
    base_url = url.split('#')[0].strip()
    if not base_url:
        return  # Internal anchor, assume valid
    
    parsed = urlparse(url)
    if parsed.scheme in ('http', 'https'):
        # Web link
        try:
            # Use HEAD for efficiency, fallback to GET if needed
            response = requests.head(url, allow_redirects=True, timeout=10)
            if response.status_code == 405:  # HEAD not allowed
                response = requests.get(url, allow_redirects=True, timeout=10)
            if response.status_code == 404:
                print(f"{file_path}:{line_num}: Invalid link (404): {url}")
        except requests.RequestException:
            print(f"{file_path}:{line_num}: Invalid link (request failed): {url}")
    elif parsed.scheme == '' and base_url:  # Relative or absolute local path
        # Resolve relative path
        resolved_path = os.path.normpath(os.path.join(os.path.dirname(file_path), base_url))
        if not os.path.exists(resolved_path):
            print(f"{file_path}:{line_num}: Invalid link (file not found): {url}")
    # Other schemes like mailto, tel, etc., assume valid

def process_md_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for line_num, line in enumerate(lines, 1):
        # Find inline links: [text](url)
        inline_matches = re.finditer(r'\[([^\]]*)\]\(([^)]*)\)', line)
        for match in inline_matches:
            url = match.group(2).strip()
            if url:
                check_link(file_path, line_num, url)
        
        # Find reference definitions: [ref]: url
        ref_matches = re.finditer(r'^\s*\[([^\]]+)\]:\s*(.+)$', line, re.MULTILINE)
        for match in ref_matches:
            url = match.group(2).strip()
            if url:
                check_link(file_path, line_num, url)

def main(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                process_md_file(file_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check links in Markdown files.')
    parser.add_argument('directory', nargs='?', default='.', help='Directory to scan (default: current)')
    args = parser.parse_args()
    main(args.directory)