##
# @file install_requirements.py
# @brief Installs all required Python libraries from requirements.txt
#
# @details
# This script reads a requirements.txt file and installs all listed packages
# using pip. It can be run from the command line or embedded in another Python process.
#
# Example usage:
#   python install_requirements.py
#
# Make sure 'requirements.txt' is in the same folder as this script.
#
# @author Assistant
# @date 2025-05-03
##

##
# @file requirements.py
# @brief Installs required Python packages from a requirements.txt file.
#
# This script ensures all necessary dependencies are installed automatically before the
# forecasting application is executed. It reads the `requirements.txt` file and uses
# `pip` to install packages.

import subprocess  # Used to run shell commands
import sys         # Provides access to Python runtime
import os          # Handles file system operations

##
# @brief Installs Python packages listed in a given requirements file.
#
# @param file_path Path to the requirements file (default is "requirements.txt").
# @return None. Prints status messages during installation.
def install_requirements(file_path="General/requirements.txt"):
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return

    print(f"📦 Installing packages from {file_path}...\n")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", file_path])
        print("\n✅ All required packages installed successfully.")
    except subprocess.CalledProcessError as e:
        print("\n❌ Error occurred during installation.")
        print(e)

##
# @brief Main entry point for installing packages if run directly.
#
# Calls `install_requirements()` using the default file path.
if __name__ == "__main__":
    install_requirements()