#!/usr/bin/bash

KEY_PATH="$HOME/Documents/android/stable.jks"
KEY_ALIAS='key0'
APK_FILE="$1"
OUTPUT="$2"

zipalign -v 4 $APK_FILE "$OUTPUT/app-release-aligned.apk"
apksigner sign --ks "$KEY_PATH" --ks-key-alias "$KEY_ALIAS" --out "$OUTPUT/app-release-signed.apk" "$OUTPUT/app-release-aligned.apk"
if ( apksigner verify "$OUTPUT/app-release-signed.apk" ); then
  echo "Successfully signed $OUTPUT/app-release-signed.apk"
else
  echo "Failed to sign $OUTPUT/app-release-signed.apk"
fi
