#!/bin/bash
#This script was designe to automatically number sentences containing dialogues for theater plays.
#Usage: ./NumberDialogue.sh PersonA: PersonB: PersonC: ... Filename

# Check usage
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 \"Prefix1: Prefix2: ...\" <Filename>"
  exit 1
fi

PREFIXES="$1"
FILE="$2"

# Check file exists
if [ ! -f "$FILE" ]; then
  echo "Error: File '$FILE' not found."
  exit 1
fi

# Convert space-separated prefixes into regex OR pattern
PATTERN="^($(echo "$PREFIXES" | sed 's/ /|/g'))"

# Generate output filename: "file.txt" → "file-Numbered.txt"
DIR=$(dirname "$FILE")
BASENAME=$(basename "$FILE")
NAME="${BASENAME%.*}"
EXT="${BASENAME##*.}"

# Handle files without an extension
if [ "$NAME" = "$EXT" ]; then
  OUTFILE="${DIR}/${NAME}-Numbered.txt"
else
  OUTFILE="${DIR}/${NAME}-Numbered.${EXT}"
fi

# Process and write to new file
awk -v pattern="$PATTERN" '
BEGIN { count=1 }
{
  if ($0 ~ pattern) {
    printf("%03d %s\n", count, $0)
    count++
  } else {
    print $0
  }
}
' "$FILE" > "$OUTFILE"
