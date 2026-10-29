# CHANGE RECORD (Part 3): Video Gallery playback
Date: 28-10-2026

## Server (Django): NO CHANGE
No Django files changed for this part. Nothing to deploy on the production server.
(It uses the existing `/mobi/videos/` API, `VideoGalleryView`.)

## What the app does now when a video card is tapped
| Video link (Vlink) | Action |
|---|---|
| YouTube (`youtube.com/watch?v=`, `youtu.be/`, `/shorts/`, `/embed/`) | Opens in the **YouTube app** (browser if YouTube isn't installed) |
| Google Drive file (`drive.google.com/file/d/...`) | Plays **inside the app** (VideoPlayer screen, Media3 ExoPlayer) |
| Video file link (`.mp4 .m4v .mkv .webm .3gp .mov .avi .m3u8`) | Plays **inside the app** |
| `/media/...` path on our server | Plays inside the app (`https://mithran.co.in` is added in front) |
| Google Drive folder | Opens in the browser / Drive app |
| Any other web page | Opens in the browser |
If a video can't be played, the player shows "Unable to play this video. Tap here to open it in the browser."

### Why in-app and not the phone's player
On a test (Pixel emulator), the only player was Google Photos, and it refused web links ("Can't play this video").
Many phones are the same, so videos now play inside the app with Media3 ExoPlayer. That works on every phone with nothing to install.
It has play/pause, a seek bar, ±10s skip, rotation (portrait and landscape) and keeps the screen on.

## Drive video sharing (IMPORTANT)
Each Drive video file must be shared as **Anyone with the link → Viewer**.
The app streams it from:
`https://drive.usercontent.google.com/download?id=<FILE_ID>&export=download&confirm=t`
- Private files won't play (the player shows an error).
- Large files work (`confirm=t` skips Drive's "can't scan for viruses" page).
- Drive limits how many times a public file can be downloaded per day. For very popular or very large videos, YouTube (unlisted) is more reliable.

## Bug fixed: video cards were blank
`model/GalleryItem.kt` expected JSON keys `v_title`, `v_link`, ... but Django sends `VTitle`, `Vlink`, ...
(the same bug as `PhotoItem.kt` in Part 1). All the keys were corrected:
```kotlin
data class GalleryItem(
    @SerializedName("VThumbnail") val VThumbnail: String?,
    @SerializedName("VTitle")     val VTitle: String?,
    @SerializedName("Vdate")      val Vdate: String?,
    @SerializedName("Vdesc")      val Vdesc: String?,
    @SerializedName("Vlink")      val Vlink: String?,
    @SerializedName("Vpostdate")  val Vpostdate: String?,
    @SerializedName("Vschool")    val Vschool: Vschool?,
    val id: String?,
    val status: String?
)
```

## Android files changed (Mithra app)
- `model/GalleryItem.kt`: JSON key fix (above)
- `GalleryAdapter.kt`:
  - new click logic (table above)
  - new functions `openYouTube()`, `playInPhonePlayer()`, `openInBrowser()`, `isVideoFile()`, `driveStreamUrl()`
  - the Drive folder regex also accepts `/drive/u/0/folders/`
- `VideoPlayer.kt`: **rewritten to use Media3 ExoPlayer** (same class name, same `videoLink` extra, new optional `fallbackLink` extra). YouTube links passed to it still open the YouTube app.
- `res/layout/activity_video_player.xml`: `VideoView`/`WebView` replaced by `androidx.media3.ui.PlayerView`, plus a loading spinner and an error text (`btnBack` kept)
- `AndroidManifest.xml`: VideoPlayer `screenOrientation` changed from `landscape` to `fullSensor`, plus `configChanges` (video keeps playing on rotation)
- `app/build.gradle.kts`: added
  ```
  implementation("androidx.media3:media3-exoplayer:1.5.1")
  implementation("androidx.media3:media3-exoplayer-hls:1.5.1")
  implementation("androidx.media3:media3-ui:1.5.1")
  ```

Backups: `Mithra/_backup_slideshow_20261028/` (`GalleryAdapter.kt`, `GalleryItem.kt`, `VideoPlayer.kt`, `activity_video_player.xml`, plus `*.v2` copies of build.gradle.kts / AndroidManifest.xml / GalleryAdapter.kt taken before the Media3 change)

## Tested (28-10-2026, Pixel 9 emulator, local server)
- Video gallery cards show their title, description and thumbnail ✔
- Sample entry "Sample Video (test)" (VideoGallery id 16, Demo school), link `https://www.w3schools.com/html/mov_bbb.mp4` → plays inside the app ✔
- Delete the sample entry after testing (Django admin → Video gallerys → id 16).

## Test on a phone
1. Add a VideoGallery entry with a YouTube link → tap → the YouTube app opens.
2. Add an entry with a Drive video link (shared as "Anyone with the link") → tap → it plays inside the app.
3. Add an entry with an `.mp4` link → tap → it plays inside the app.
4. Check that the video cards now show their title, description and thumbnail.

## Release
Goes out in the same APK as Parts 1 and 2: Gradle sync → `Auth.kt` production URLs → bump versionCode → signed build.
