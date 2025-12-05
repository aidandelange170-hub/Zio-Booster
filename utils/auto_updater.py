import requests
import json
import os
import sys
import subprocess
import zipfile
import tempfile
import shutil
from packaging import version
import logging

class AutoUpdater:
    def __init__(self, repo_owner, repo_name, current_version, install_path=None):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.current_version = current_version
        self.install_path = install_path or os.getcwd()
        self.api_url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/releases"
        self.logger = logging.getLogger(__name__)
        
    def get_latest_release(self):
        """Fetch the latest release from GitHub API"""
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            releases = response.json()
            
            if not releases:
                self.logger.warning("No releases found")
                return None
                
            # Get the latest release (first in the list as GitHub returns them in chronological order)
            latest_release = releases[0]
            return {
                'version': latest_release['tag_name'],
                'name': latest_release['name'],
                'published_at': latest_release['published_at'],
                'assets': latest_release['assets'],
                'download_url': latest_release['zipball_url']
            }
        except requests.RequestException as e:
            self.logger.error(f"Error fetching releases: {e}")
            return None
        except json.JSONDecodeError as e:
            self.logger.error(f"Error parsing JSON response: {e}")
            return None
    
    def is_new_version_available(self):
        """Check if a newer version is available"""
        latest_release = self.get_latest_release()
        if not latest_release:
            return False, None
            
        try:
            current_ver = version.parse(self.current_version)
            latest_ver = version.parse(latest_release['version'])
            
            if latest_ver > current_ver:
                self.logger.info(f"New version available: {latest_release['version']} > {self.current_version}")
                return True, latest_release
            else:
                self.logger.info(f"Current version is up to date: {self.current_version}")
                return False, None
        except Exception as e:
            self.logger.error(f"Error comparing versions: {e}")
            return False, None
    
    def download_and_install_update(self, release_info):
        """Download and install the update"""
        try:
            download_url = release_info['download_url']
            self.logger.info(f"Downloading update from: {download_url}")
            
            # Create temporary directory for download
            with tempfile.TemporaryDirectory() as temp_dir:
                zip_path = os.path.join(temp_dir, "update.zip")
                
                # Download the release
                response = requests.get(download_url, stream=True)
                response.raise_for_status()
                
                with open(zip_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                # Extract the zip file
                extract_dir = os.path.join(temp_dir, "extracted")
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_dir)
                
                # Find the extracted folder (GitHub archives have a root folder with repo name)
                extracted_folders = os.listdir(extract_dir)
                if extracted_folders:
                    source_dir = os.path.join(extract_dir, extracted_folders[0])
                    
                    # Backup current installation
                    backup_dir = os.path.join(self.install_path, f"backup_{self.current_version}")
                    if os.path.exists(backup_dir):
                        shutil.rmtree(backup_dir)
                    shutil.copytree(self.install_path, backup_dir, 
                                  ignore=shutil.ignore_patterns('backup_*', '.git', '__pycache__', '*.pyc'))
                    
                    # Copy new files to installation directory
                    self._copy_new_files(source_dir, self.install_path)
                    
                    self.logger.info(f"Update installed successfully to {self.install_path}")
                    return True
                else:
                    self.logger.error("No files extracted from the update archive")
                    return False
                    
        except Exception as e:
            self.logger.error(f"Error during update: {e}")
            return False
    
    def _copy_new_files(self, source_dir, dest_dir):
        """Copy new files from source to destination, preserving existing config files"""
        for item in os.listdir(source_dir):
            source_item = os.path.join(source_dir, item)
            dest_item = os.path.join(dest_dir, item)
            
            # Skip certain files/folders that should not be overwritten
            if item in ['.git', '__pycache__', 'backup_*']:
                continue
                
            # Skip config files that might have user modifications
            if item in ['config.json', 'settings.json', 'preferences.json']:
                if os.path.exists(dest_item):
                    continue  # Keep existing config file
            
            if os.path.isdir(source_item):
                if os.path.exists(dest_item):
                    shutil.rmtree(dest_item)
                shutil.copytree(source_item, dest_item)
            else:
                shutil.copy2(source_item, dest_item)
    
    def run_update_check(self):
        """Main method to run the update check and install if needed"""
        self.logger.info("Checking for updates...")
        is_available, release_info = self.is_new_version_available()
        
        if is_available:
            self.logger.info(f"New version {release_info['version']} is available")
            success = self.download_and_install_update(release_info)
            if success:
                self.logger.info("Update completed successfully!")
                return True
            else:
                self.logger.error("Update failed!")
                return False
        else:
            self.logger.info("No new version available")
            return False

# Example usage
def check_for_updates():
    """Check for updates and install if available"""
    updater = AutoUpdater(
        repo_owner="aidandelange170-hub",
        repo_name="Zio-Booster",
        current_version="1.0.0",  # This should be dynamically determined
        install_path=os.getcwd()
    )
    
    return updater.run_update_check()

if __name__ == "__main__":
    check_for_updates()