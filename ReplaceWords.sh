#!/bin/bash
#This script replaces all instances of OldWord with NewWord in any Filename passed to it. 
#Typically used for simple text files. Only exact matches (whole words) will be replaced.

# Check for correct number of arguments
if [ "$#" -ne 3 ]; then
  echo "Usage: $0 <OldWord> <NewWord> <Filename>"
  exit 1
fi

OLD_WORD="$1"
NEW_WORD="$2"
FILE="$3"

# Check if the file exists
if [ ! -f "$FILE" ]; then
  echo "Error: File '$FILE' not found."
  exit 1
fi

# Replace whole word occurrences using word boundaries
sed -i "s/\\b$OLD_WORD\\b/$NEW_WORD/g" "$FILE"

echo "Replaced all instances of '$OLD_WORD' with '$NEW_WORD' in '$FILE'."