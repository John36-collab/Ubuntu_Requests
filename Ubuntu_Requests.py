"""
Ubuntu Image Fetcher - Enhanced Edition
A tool for mindfully collecting images from the web while respecting Ubuntu principles
"""

import requests
import os
import hashlib
from urllib.parse import urlparse
import mimetypes
from pathlib import Path

def calculate_file_hash(filepath):
    """Calculate MD5 hash of a file to check for duplicates"""
    hash_md5 = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except IOError:
        return None

def is_duplicate_image(content, directory):
    """Check if image already exists in directory by comparing hashes"""
    # Calculate hash of the new content
    new_hash = hashlib.md5(content).hexdigest()
    
    # Check all files in directory for matching hash
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            existing_hash = calculate_file_hash(filepath)
            if existing_hash == new_hash:
                return True, filename
    
    return False, None

def is_safe_to_download(url, response):
    """Implement safety checks before downloading files"""
    # Check content type to ensure it's an image
    content_type = response.headers.get('content-type', '')
    if not content_type.startswith('image/'):
        return False, f"Content type is not an image: {content_type}"
    
    # Check file size (limit to 10MB for safety)
    content_length = response.headers.get('content-length')
    if content_length and int(content_length) > 10 * 1024 * 1024:  # 10MB
        return False, "File size exceeds safety limit (10MB)"
    
    # Check for common image extensions in URL as additional safety measure
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff']
    parsed_url = urlparse(url)
    path = parsed_url.path.lower()
    if not any(path.endswith(ext) for ext in image_extensions):
        # This is just a warning, not a block, as some URLs might not have extensions
        print("   Warning: URL doesn't contain a common image extension")
    
    return True, "Safe to download"

def get_filename_from_url(url, response):
    """Extract filename from URL or generate one based on content"""
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    
    # If no filename in URL, try to get it from content-disposition header
    if not filename or '.' not in filename:
        content_disp = response.headers.get('content-disposition', '')
        if 'filename=' in content_disp:
            filename = content_disp.split('filename=')[1].strip('"\'')
    
    # If still no filename, generate one based on content type
    if not filename or '.' not in filename:
        content_type = response.headers.get('content-type', 'image/jpeg')
        ext = mimetypes.guess_extension(content_type.split(';')[0]) or '.jpg'
        filename = f"downloaded_image{ext}"
    
    # Clean filename to remove any query parameters or problematic characters
    filename = filename.split('?')[0].split('#')[0]
    safe_chars = " -_.()[]{}abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    filename = ''.join(c for c in filename if c in safe_chars).strip()
    
    # Ensure filename has an extension
    if '.' not in filename:
        content_type = response.headers.get('content-type', 'image/jpeg')
        ext = mimetypes.guess_extension(content_type.split(';')[0]) or '.jpg'
        filename += ext
    
    return filename

def download_single_image(url, directory):
    """Download a single image with safety checks"""
    try:
        print(f"\n  Processing: {url}")
        
        # Send HEAD request first to check headers before downloading
        try:
            head_response = requests.head(url, timeout=10, allow_redirects=True)
            head_response.raise_for_status()
        except requests.exceptions.RequestException:
            # If HEAD fails, try GET but we'll need to be careful with the content
            pass
        
        # Download the image with stream=True to control the download
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        
        # Check if safe to download
        is_safe, message = is_safe_to_download(url, response)
        if not is_safe:
            print(f" Safety check failed: {message}")
            return False
        
        # Get the image content
        content = response.content
        
        # Check for duplicates
        is_dup, existing_filename = is_duplicate_image(content, directory)
        if is_dup:
            print(f" Skipping duplicate of existing image: {existing_filename}")
            return True
        
        # Get appropriate filename
        filename = get_filename_from_url(url, response)
        filepath = os.path.join(directory, filename)
        
        # Handle filename conflicts
        counter = 1
        original_filepath = filepath
        while os.path.exists(filepath):
            name, ext = os.path.splitext(original_filepath)
            filepath = f"{name}_{counter}{ext}"
            counter += 1
        
        # Save the image
        with open(filepath, 'wb') as f:
            f.write(content)
        
        print(f" Successfully fetched: {os.path.basename(filepath)}")
        print(f" Image saved to {filepath}")
        return True
        
    except requests.exceptions.RequestException as e:
        print(f" Connection error: {e}")
    except Exception as e:
        print(f" An error occurred: {e}")
    
    return False

def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")
    
    # Create directory if it doesn't exist
    directory = "Fetched_Images"
    os.makedirs(directory, exist_ok=True)
    print(f" Using directory: {directory}")
    
    # Get URLs from user
    urls_input = input("Please enter image URL(s), separated by commas: ").strip()
    
    if not urls_input:
        print(" No URLs provided. Exiting.")
        return
    
    urls = [url.strip() for url in urls_input.split(',') if url.strip()]
    
    successful_downloads = 0
    total_urls = len(urls)
    
    print(f"\n  Processing {total_urls} image(s)...")
    
    for i, url in enumerate(urls, 1):
        print(f"\n[{i}/{total_urls}] ", end="")
        if download_single_image(url, directory):
            successful_downloads += 1
    
    # Summary
    print("\n" + "="*50)
    print("Download Summary:")
    print(f"✓ Successful downloads: {successful_downloads}/{total_urls}")
    
    if successful_downloads > 0:
        print("\nConnection strengthened. Community enriched.")
    else:
        print("\nNo images were downloaded. Please check your URLs and try again.")

if __name__ == "__main__":
    main()
