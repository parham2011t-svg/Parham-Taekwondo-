# Parham Taekwondo - Android APK project

This is a Kivy rewrite of the original Pygame sample so it can be packaged for Android.

## Files
- `main.py`: Kivy game code.
- `buildozer.spec`: Android packaging configuration.
- `.github/workflows/android.yml`: cloud build workflow using GitHub Actions.

## Build APK using GitHub Actions (phone-friendly upload path)
1. Create a GitHub account if you do not already have one.
2. Create a new **public or private** repository.
3. Upload the contents of this folder to the repository, keeping `.github/workflows/android.yml` in that exact path.
4. Open the repository's **Actions** tab.
5. Choose **Build Android APK** and tap **Run workflow**.
6. Wait for the run to finish. Open the successful run and download the artifact named `parham-taekwondo-apk`.
7. Extract the downloaded ZIP; it contains the APK.

The cloud build downloads Android build dependencies, so it does not use your phone's 50 MB data allowance for the large SDK/NDK downloads. It does require internet to upload the source and download the finished APK.

## Notes
- First build may take several minutes.
- This is a debug APK for testing/sharing, not a Play Store release.
- Android may ask to allow installation from the browser/files app.
- The code is a prototype. The controls, layout and gameplay should be tested on a real phone; touch controls are provided by Kivy buttons.
