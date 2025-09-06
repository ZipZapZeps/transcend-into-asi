import os
import re
import requests
from urllib.parse import urljoin, urlparse
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def is_valid_url(url):
    """Check if a URL is valid by making a HEAD request."""
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        return response.status_code != 404
    except requests.RequestException as e:
        logger.error(f"Error checking URL {url}: {e}")
        return False

def resolve_relative_path(base_path, relative_path):
    """Resolve a relative path to an absolute path."""
    base = Path(base_path).parent
    resolved = (base / relative_path).resolve()
    return resolved

def is_valid_file_path(file_path):
    """Check if a file path exists."""
    return Path(file_path).exists()

def extract_links_from_markdown(content, file_path):
    """Extract all links from markdown content."""
    # Regex to match markdown links [text](url)
    link_pattern = r'\[([^\]]*)\]\(([^)]+)\)'
    links = []
    
    for match in re.finditer(link_pattern, content):
        url = match.group(2).strip()
        # Skip anchor links
        if url.startswith('#'):
            continue
        # Handle relative paths
        if not url.startswith(('http://', 'https://')):
            resolved_path = resolve_relative_path(file_path, url)
            if resolved_path.exists():
                links.append(('file', str(resolved_path)))
            else:
                links.append(('file', str(resolved_path)))
        else:
            links.append(('url', url))
    
    return links

def check_markdown_files(directory):
    """Check all markdown files in directory and subdirectories for valid links."""
    directory = Path(directory)
    invalid_links = []
    
    # Walk through directory
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = Path(root) / file
                logger.info(f"Checking file: {file_path}")
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    links = extract_links_from_markdown(content, file_path)
                    
                    for link_type, link in links:
                        if link_type == 'url':
                            logger.info(f"Checking URL: {link}")
                            if not is_valid_url(link):
                                invalid_links.append((str(file_path), link, "URL not accessible or returns 404"))
                        elif link_type == 'file':
                            logger.info(f"Checking file link: {link}")
                            if not is_valid_file_path(link):
                                invalid_links.append((str(file_path), link, "File does not exist"))
                
                except Exception as e:
                    logger.error(f"Error processing file {file_path}: {e}")
                    invalid_links.append((str(file_path), None, f"Error reading file: {e}"))
    
    return invalid_links

def main():
    # Get directory from user or use current directory
    directory = input("Enter directory to scan (default: current directory): ") or "."
    
    logger.info(f"Scanning markdown files in {directory}")
    invalid_links = check_markdown_files(directory)
    
    if invalid_links:
        logger.warning("\nFound invalid or broken links:")
        for file_path, link, error in invalid_links:
            if link:
                logger.warning(f"In {file_path}: {link} - {error}")
            else:
                logger.warning(f"In {file_path}: {error}")
    else:
        logger.info("\nAll links are valid!")

if __name__ == "__main__":
    main()