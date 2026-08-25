name: Build Android APK

on:
  workflow_dispatch:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-22.04

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install system dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y \
            git zip unzip wget curl \
            openjdk-17-jdk \
            autoconf automake libtool pkg-config \
            zlib1g-dev libncurses5-dev libncursesw5-dev \
            cmake libffi-dev libssl-dev

      - name: Install Android command line tools
        run: |
          mkdir -p "$HOME/android-sdk/cmdline-tools"
          cd "$HOME/android-sdk"
          
          wget -q https://dl.google.com/android/repository/commandlinetools-linux-13114758_latest.zip
          unzip -q commandlinetools-linux-13114758_latest.zip
          
          mkdir -p cmdline-tools/latest
          mv cmdline-tools/* cmdline-tools/latest/ 2>/dev/null || true

          echo "ANDROID_HOME=$HOME/android-sdk" >> $GITHUB_ENV
          echo "ANDROID_SDK_ROOT=$HOME/android-sdk" >> $GITHUB_ENV
          echo "$HOME/android-sdk/cmdline-tools/latest/bin" >> $GITHUB_PATH
          echo "$HOME/android-sdk/platform-tools" >> $GITHUB_PATH
          echo "$HOME/android-sdk/build-tools/35.0.0" >> $GITHUB_PATH

      - name: Install Android SDK packages
        run: |
          yes | sdkmanager --licenses || true
          sdkmanager \
            "platform-tools" \
            "platforms;android-35" \
            "build-tools;35.0.0"

      - name: Install Python dependencies
        run: |
          python -m pip install --upgrade pip
          pip install buildozer cython

      - name: Build APK
        run: |
          buildozer android debug

      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: Detector-Magnetico-APK
          path: bin/*.apk
