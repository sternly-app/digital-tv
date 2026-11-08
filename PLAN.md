# Plan: folder photo carousel and live Spotify card

## Requirements (agreed)
- Left frame: carousel of photos the owner drops into `photos/`. No upload step needed on the TV.
- Right card: the song playing on the owner's Spotify account right now (cover, title, artist, progress, device), with previous, play/pause, next and volume.
- Spotify login prompt on the page. Owner has Premium. Music plays on a phone or speaker (Spotify Connect). The TV page is the remote and display, not the player.
- Both boxes stay the current size (`--side` by `--side * 1.12`). Must fit at 1280x720.
- Runs in the LG webOS browser (Chromium 79+ on webOS 6, newer on webOS 22+). Golden theme, no emoji, no purple or pink.
- Done when it is verified in a separate browser: the login prompt appears, the carousel cycles test images, and the card renders playing / idle / logged-out states.

## Research findings that shape the design
- A static page cannot list a folder. Use a manifest `photos/photos.js` (`window.PHOTOS = [...]`) loaded by a script tag. It works on GitHub Pages and on file://. `scripts/make_photos.py` writes it.
- webOS 6 (Chromium 79) does not apply EXIF rotation. The script's `--shrink` option (needs Pillow) bakes in rotation and resizes to 1200px. Keep photos to about 1200px and under 300 KB.
- Crossfade with two images. Decode the next image before fading. `object-fit: cover`.
- Spotify: Authorization Code with PKCE from the page, no secret. Scopes `user-read-playback-state user-read-currently-playing user-modify-playback-state`. Poll `GET /v1/me/player` every 4 s and animate progress in between. Controls need Premium. A 404 means no active device, so show a device list with a transfer option.
- Redirect URIs must match exactly. HTTPS, or `http://127.0.0.1:PORT/`. `localhost` is rejected. Register both the GitHub Pages URL and `http://127.0.0.1:8000/`.
- Refresh tokens last 6 months from login. After that, log in again.
- The Web Playback SDK needs Widevine and is not supported on webOS. Skip it.
- `crypto.subtle` exists only in secure contexts. Include a small JS SHA-256 fallback.
- No device-code flow. Log in once on the TV, or log in on a laptop and paste the login code into the TV's settings.

## Build steps
1. `photos/photos.js` plus a `<script src="photos/photos.js">` tag. The slideshow uses folder photos first, then any uploaded ones. Add decode-before-fade, a small counter, `keyCode` support for the LG remote and `preventDefault` on the arrows.
2. `scripts/make_photos.py`: scans `photos/` and writes `photos.js`. `--shrink` resizes and rotates in place (Pillow).
3. Spotify card replaces the embed by default. States: not set up (enter Client ID), logged out (Connect button), idle (device list), playing (cover, text, progress, controls). Settings: Client ID, redirect URI shown for copying, disconnect, login code copy and paste, and a toggle to use the old embed player instead.
4. Remote keys: Play 415, Pause 19, play/pause toggle 10252, FF 417 for next, RW 412 for previous. Arrows stay for photos.
5. Update CLAUDE.md and README.

## Test plan
- `scripts/check_js.py`.
- Serve on `http://127.0.0.1:8000/` and open in a separate headless Chrome:
  - The carousel cycles generated test photos (portrait and landscape) at 1920x1080 and 1280x720.
  - Logged out: the Connect button goes to `accounts.spotify.com/authorize` with the right parameters.
  - Playing and idle states, using stubbed API responses injected by the test script (nothing in index.html), screenshotted at both sizes.
- Not testable here: a real login (needs the owner's Client ID) and the LG hardware.

## Owner setup (once)
1. developer.spotify.com/dashboard > Create app > Web API. Redirect URIs: `https://<user>.github.io/<repo>/` and `http://127.0.0.1:8000/`.
2. Settings > User Management: add your Spotify email.
3. Copy the Client ID into the page settings, or set `CLIENT_ID` at the top of the script.
