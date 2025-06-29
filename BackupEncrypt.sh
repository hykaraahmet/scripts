#!/bin/bash
#This script creates and encrypted tar.gz archive of a specified folder.
#It is good for backing up important folders to USB disks or cloud storage.
#To run it: ./backup_encrypt.sh /path/to/folder yourpassword
#To decrypt the file later: gpg -d /path/to/backup_YYYYMMDD_HHMMSS.tar.gz.gpg > backup_YYYYMMDD_HHMMSS.tar.gz
#Author: Hasan Y. Karaahmet
#Version 1.1


# Function to display usage
usage() {
    echo "Usage: $0 <full_path_to_folder> <password>"
    echo "Example: $0 /home/user/documents mysecretpassword"
    exit 1
}

# Check if correct number of arguments is provided
if [ "$#" -ne 2 ]; then
    usage
fi

# Assign variables
FOLDER_PATH="$1"
PASSWORD="$2"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="backup_${TIMESTAMP}.tar.gz"
ENCRYPTED_NAME="backup_${TIMESTAMP}.tar.gz.gpg"
PARENT_DIR=$(dirname "$FOLDER_PATH")

# Check if folder exists
if [ ! -d "$FOLDER_PATH" ]; then
    echo "Error: Directory '$FOLDER_PATH' does not exist."
    exit 1
fi

# Check if folder is readable
if [ ! -r "$FOLDER_PATH" ]; then
    echo "Error: Directory '$FOLDER_PATH' is not readable."
    exit 1
fi

# Check if parent directory is writable
if [ ! -w "$PARENT_DIR" ]; then
    echo "Error: Parent directory '$PARENT_DIR' is not writable."
    exit 1
fi

# Check if tar and gpg are installed
if ! command -v tar &> /dev/null; then
    echo "Error: tar is not installed."
    exit 1
fi
if ! command -v gpg &> /dev/null; then
    echo "Error: gpg is not installed."
    exit 1
fi

# Create temporary tar.gz archive
echo "Creating backup archive..."
if ! tar -czf "/tmp/$BACKUP_NAME" -C "$FOLDER_PATH" . 2>/dev/null; then
    echo "Error: Failed to create tar.gz archive."
    rm -f "/tmp/$BACKUP_NAME"
    exit 1
fi

# Encrypt the archive
echo "Encrypting backup..."
echo "$PASSWORD" | gpg --batch --yes --passphrase-fd 0 -c "/tmp/$BACKUP_NAME" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Error: Failed to encrypt archive."
    rm -f "/tmp/$BACKUP_NAME"
    exit 1
fi

# Move encrypted file to parent directory
if ! mv "/tmp/$ENCRYPTED_NAME" "$PARENT_DIR/$ENCRYPTED_NAME" 2>/dev/null; then
    echo "Error: Failed to move encrypted archive to '$PARENT_DIR'."
    rm -f "/tmp/$BACKUP_NAME" "/tmp/$ENCRYPTED_NAME"
    exit 1
fi

# Clean up temporary tar file
rm -f "/tmp/$BACKUP_NAME"

# Success message
echo "Success: Encrypted backup created at '$PARENT_DIR/$ENCRYPTED_NAME'"
echo "To decrypt, use: gpg -d '$PARENT_DIR/$ENCRYPTED_NAME' > $BACKUP_NAME"
