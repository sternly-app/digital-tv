# Diwali TV screensaver

A single-file static web page (`index.html`, no build step, no dependencies) that shows a Diwali scene full screen on an LG webOS TV. External loads: Google Fonts, the Spotify Web API and accounts service, and Spotify's embed iframe (only in embed mode).

## Owner requirements (do not break these)
- Golden theme: warm brown-black, gold, amber, ivory. The rangoli is multicolor (orange, yellow, red, green, teal). **Strictly no purple, pink, plum or similar.**
- "Happy Diwali" greeting in a square box at the center, with Devanagari line, large type.
- Colorful rangoli in the background that always rotates and never clips.
- Photo frame (bottom left): crossfade carousel of the photos in `photos/` (listed in `photos/photos.js`). Without folder photos it shows "Add photos" for uploads. Spotify card (bottom right) is exactly the same size as the photo frame.
- Spotify card shows the song playing on the owner's account (cover, title, artist, progress, device) with previous, play/pause, next and volume. Owner has Premium. Music plays on a phone or speaker; the page is a remote and display. The old embed player is kept as a settings toggle.
- Must run directly on the TV: always full screen, never auto-off or screensaver, shown all the time. No on-screen "press OK" message.
- Classy and restrained. No emoji.

## Layout and files
- `index.html`: the whole app. Sections in the script, in order: settings and `localStorage`, garland SVG, background rangoli (SMIL), diyas, fireworks canvas loop, clock, Spotify embed, Spotify live (PKCE login, polling, controls), pictures (folder + IndexedDB + slideshow), settings panel, fullscreen and wake lock, keep-awake video, keys, idle UI hiding.
- `photos/`: the owner's photos plus `photos.js` (generated list). `sample-0*.jpg` are test images, delete them before deploying.
- `scripts/make_photos.py`: rewrites `photos/photos.js`. `--shrink` resizes to 1200px and bakes in EXIF rotation (Pillow). Run after changing photos.
- `PLAN.md`: the plan and research behind the carousel and Spotify card.
- `diwali-tv.html`: an older copy of the app, not referenced anywhere.
- `archive/slow-drift.html`, `archive/diwali-lights.html`: earlier iterations, kept for reference only. They were claude.ai artifacts (iframes blocked, so Spotify was links only). Do not edit.
- `scripts/check_js.py`: extracts the inline script and runs `node --check`. Run it after every edit.

## Layers (z-index, back to front)
`#rangoli` 2, `#fw` canvas 3, `#garland` 4, `#center` box 5, `#diyas` 6, `#clock` `#photo` `#music` 7, `#gear` 20, `#panel` 30.

## Key CSS variables
`--box` greeting box size, `--u` is `--box / 100` (all box text uses `calc(var(--u) * N)`), `--side` is the photo frame and Spotify card width (height is `--side * 1.12`), `--floor` is space reserved for the diya row.

## State
- `localStorage` key `diwalitv.v2`. Fields: `fw` fireworks on, `fwi` amount 1-5, `clk` show clock, `h24`, `from` signed-by text, `msg` greeting line, `pl` Spotify link (embed), `ss` slideshow on, `ssi` seconds per photo, `cmp` compact embed player, `emb` use embed instead of live card, `cid` Spotify Client ID. (`ssa` is unused.)
- `localStorage` key `diwalitv.sp`: Spotify tokens `{at, exp, rt, cid}`. `diwalitv.sp.pkce` holds the verifier during login.
- IndexedDB database `diwalitv`, store `photos` (blobs, downscaled to 1600px JPEG). If IndexedDB fails, photos live in memory only.
- Everything is per browser. Nothing is uploaded anywhere.

## Constraints
- **Old webOS browsers (Chromium about 79+):** avoid container queries, `aspect-ratio`, flex `gap` in main layout, `inset`, `color-mix`. Use `calc()` with `--u`, explicit width and height, margins.
- **Rotation uses SMIL `animateTransform`** on the rangoli groups. CSS `transform-box` rotation orbited off-center and clipped. Do not go back to it.
- **Spotify live card:** Web API, Authorization Code with PKCE, no secret. Scopes `user-read-playback-state user-read-currently-playing user-modify-playback-state`. Polls `GET /v1/me/player` every 4 s while playing, 12 s idle, 30 s when hidden; honors 429 Retry-After. Controls need Premium (403 shows a message). 204/no item shows the idle view with a device list (`PUT /me/player` to transfer). Redirect URI is `location.origin + location.pathname` and must be registered exactly (HTTPS, or `http://127.0.0.1:PORT/`; `localhost` is rejected). Development-mode apps need the owner to have Premium and list the user under User Management (max 5). Refresh tokens expire 6 months after login. `CLIENT_ID` constant at the top of the section can hard-code the ID. The "login code" (`clientid:refreshtoken`) moves a laptop login to the TV. A pure-JS SHA-256 fallback covers browsers without `crypto.subtle`. Do not use the Web Playback SDK (needs Widevine, not supported on webOS).
- **LG remote keys:** Left/Right 37/39 change photo; Play 415, Pause 19, Play/Pause 10252, FF 417 next, RW 412 previous.
- **EXIF:** Chromium below 81 (webOS 6) ignores photo rotation, so run `make_photos.py --shrink`.
- **Spotify embed (fallback mode):** the embed URL is `https://open.spotify.com/embed/{type}/{id}?utm_source=generator&theme=0`. Full songs need a Spotify login in the same browser, otherwise 30-second previews and a "Get Spotify" overlay that cannot be removed. The embed cannot report what is playing, and it cannot show songs playing in the Spotify app. A live now-playing display would need the Spotify Web API (PKCE login, a free developer app, hosted HTTPS redirect URI).
- **Fullscreen** needs a user gesture. The page goes full screen quietly on the first click or Enter. Kiosk apps avoid the gesture.
- **Keep-awake** (wake lock plus a tiny muted canvas-stream video) is best effort and unproven on LG. LG's browser has been reported to idle after about 40 minutes regardless. The TV setting General > System > Time and Timer > Timers > Auto Power Off after 4 hours should be off.
- The claude.ai preview pane blocks iframes, so the player shows a broken icon there. Test in Chrome.

## Known gaps and cleanup
- Never tested on real LG hardware. webOS version compatibility unknown.
- Unused CSS (`.spin`, `.spinf`) and the unused `ssa` default.
- Fireworks run continuously. CPU cost on a TV is unmeasured. Particle cap 700, canvas DPR capped at 1.25.

## Testing
1. `python3 scripts/check_js.py` (needs node).
2. Open `index.html` in desktop Chrome. Check at 1920x1080 and 1280x720, and a narrow portrait width (card stacks, photo frame hidden).
3. Serve with `python3 -m http.server 8000 --bind 127.0.0.1` and open `http://127.0.0.1:8000/` (needed for Spotify login; file:// cannot log in). With a Client ID set, Connect must go to accounts.spotify.com.
4. Confirm the carousel cycles the folder photos and Left/Right work.
5. Embed mode: toggle it in settings, paste a playlist link, press LOAD.
6. Last verified 2026-11-08 in headless Chrome 156 with a stubbed Spotify API (playing, idle, controls, 403, login code, token exchange) at 1920x1080, 1280x720 and 720x1280. A real Spotify login is untested until the owner's Client ID exists.

## Deploy
GitHub Pages: public repo, upload `index.html` and the `photos/` folder, Settings > Pages > Deploy from a branch > main > / (root). Open the `https://<user>.github.io/<repo>/` link on the TV and bookmark it. Add that exact URL (with trailing slash) as a redirect URI in the Spotify dashboard. For true always-on use, a stick with Fully Kiosk Browser or a mini PC running Chrome with `--kiosk` is more reliable than the TV's own browser.

## Possible next work
- Test on the real TV and record the webOS version and results here.
- Build the owner's message and signed-by text into the file, and set `CLIENT_ID`, so nothing needs setting up on the TV.
- Portrait layout: the Spotify card slightly overlaps the greeting box at 720x1280.
- Remove the unused code above.

## Working style
Owner is direct and efficiency-focused. Keep replies short, no filler or hedging beyond what is real, honest blunt assessments. Do not use em dashes in any copy. Make only the change asked for, and do not drift from the constraints above. Prefer natural wording over polished or AI-sounding phrasing.
