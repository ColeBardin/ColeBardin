#!/bin/sh
# Create a folder (named dmg) to prepare our DMG in (if it doesn't already exist).
mkdir -p dist/dmg
# Empty the dmg folder.
rm -r dist/dmg/*
# Copy the app bundle to the dmg folder.
cp -r "dist/Amongus.app" dist/dmg
# If the DMG already exists, delete it.
test -f "dist/Amongus.dmg" && rm "dist/Amongus.dmg"
create-dmg \
  --volname "Amongus" \
  --volicon "amongus.icns" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --icon-size 100 \
  --icon "Amongus.app" 175 120 \
  --hide-extension "Amongus.app" \
  --app-drop-link 425 120 \
  "dist/Amongus.dmg" \
  "dist/dmg/"