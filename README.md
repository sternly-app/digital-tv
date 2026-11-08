# Diwali TV screensaver

One static page, `index.html`, that shows a golden Diwali scene full screen: rotating rangoli, fireworks, marigold garland, flickering diyas, a "Happy Diwali" greeting box, a photo slideshow and a Spotify player.

## Run it
Open `index.html` in Chrome. No build, no install.

## Put it on a TV
Host `index.html` on GitHub Pages (public repo, Settings > Pages, deploy from `main`), then open the link in the TV's browser. See `CLAUDE.md` for TV settings and more reliable always-on options.

## Photos
Put photos in `photos/`, then run `python3 scripts/make_photos.py` (add `--shrink` to resize and fix rotation, needs `pip3 install pillow`).

## Spotify
1. developer.spotify.com/dashboard > Create app > Web API. Add redirect URIs `https://<user>.github.io/<repo>/` and `http://127.0.0.1:8000/`.
2. Settings > User Management: add your Spotify email. Copy the Client ID.
3. On the page: settings > Spotify > paste the Client ID > Connect Spotify. Needs Premium for the controls.
4. To skip typing on the TV: log in on a laptop, press "Show this browser's login code", and paste it into the TV's settings.

Test locally with `python3 -m http.server 8000 --bind 127.0.0.1` and open `http://127.0.0.1:8000/`.

## Controls
- **S** settings, **F** full screen, **Esc** close settings, **Left and Right** change photo. Remote **Play, Pause, FF, RW** control Spotify.
- Click the gear for settings: message, signed-by name, photos, slideshow, Spotify, fireworks, clock.

## Notes
- Settings and the Spotify login are saved in the browser you use. Nothing is uploaded.
- `archive/` holds earlier versions for reference.
- `scripts/check_js.py` syntax-checks the page script (needs node).
