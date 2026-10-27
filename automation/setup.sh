#!/bin/bash
# Copies the post images into the only folder Chrome file_upload accepts.
set -e
R="$(cd "$(dirname "$0")/.." && pwd)"
D=/mnt/user-data/uploads/snl
mkdir -p "$D"
for f in "$R"/n[0-9]*_slide_*.jpg; do b=$(basename "$f"); cp "$f" "$D/fb_${b#n}"; done
for f in "$R"/n[0-9]*_story_*.jpg; do b=$(basename "$f"); cp "$f" "$D/tk_${b#n}"; done
cp "$R/automation/video2.mp4" "$D/video2.mp4"
ls "$D" | wc -l
