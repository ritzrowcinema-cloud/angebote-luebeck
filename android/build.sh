#!/usr/bin/env bash
# Baut die APK ohne Gradle. Benötigt: Android SDK (platforms;android-34, build-tools;34.0.0), JDK, und einen Keystore.
# Nutzung: SDK=/pfad/zum/sdk KS=release.jks KSPASS=... ./build.sh
set -e
BT=$SDK/build-tools/34.0.0; AJ=$SDK/platforms/android-34/android.jar
rm -rf build && mkdir -p build/gen build/classes build/dex
$BT/aapt2 compile --dir res -o build/res.zip
$BT/aapt2 link -o build/base.apk -I $AJ --manifest AndroidManifest.xml -A assets --min-sdk-version 24 --target-sdk-version 34 --version-code 2 --version-name 2.0 --java build/gen build/res.zip
javac -nowarn -source 11 -target 11 -classpath $AJ -d build/classes -sourcepath src:build/gen $(find src build/gen -name '*.java')
$BT/d8 --release --min-api 24 --lib $AJ --output build/dex $(find build/classes -name '*.class')
cp build/base.apk build/unsigned.apk && (cd build/dex && zip -q ../unsigned.apk classes.dex)
$BT/zipalign -f -p 4 build/unsigned.apk build/aligned.apk
$BT/apksigner sign --ks "$KS" --ks-pass pass:"$KSPASS" --out Angebote-Luebeck.apk build/aligned.apk
