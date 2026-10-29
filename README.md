# SpaceAtom — pitch website

Responsive, standalone GitHub Pages website for **SpaceAtom**, an independently
developed Godot space-action game. This version adds an art-first presentation,
a real-logo integration, official character portraits, and a gameplay screenshot
gallery, with **real assets required** before those galleries appear.

## Preview locally

```sh
python3 -m http.server 8000
```

Open <http://localhost:8000>. No JavaScript framework, package manager, build
process, or API key is required.

## Adding the official game artwork

**Status:** The private game source and its original character/logo images were
not accessible to the GitHub connection during this change. Thus **no original
game images have been copied to this branch yet**. The existing illustrated
hero and outpost images are *concepts, not game screenshots*. They remain
visibly labelled until approved source files are imported.

With an authorized local checkout of the **actual SpaceAtom game repository**,
inspect filename-based asset candidates:

```sh
python3 tools/import_game_assets.py --game-root /path/to/spaceatom --dry-run
```

The importer can suggest a logo, hero image and ally/enemy outpost art based
on source image filenames. For accuracy, provide the real, verified paths
explicitly, and add character portraits/screenshots:

```sh
python3 tools/import_game_assets.py --game-root /path/to/spaceatom \
  --no-auto \
  --logo assets/REAL-LOGO.png \
  --hero assets/REAL-HERO.png \
  --ally assets/REAL-ALLY-OUTPOST.png \
  --enemy assets/REAL-ENEMY-OUTPOST.png \
  --character "Character Name=assets/REAL-CHARACTER.png" \
  --screenshot assets/REAL-SCREENSHOT.png
```

Paths above are **examples, not actual verified game filenames**. Omit options
without a verified asset; repeat `--character` and `--screenshot` as needed.
Use the canonical names from the game for the character labels. The tool
copies only images from inside the game checkout to `assets/official/` and
creates the local `assets/official/media.json` manifest.

Before committing the copied images, review their appearance, file sizes, and
licenses. Never put private repository credentials in this website. The
imported images will be publicly served by GitHub Pages.

## How the artwork presentation works

- `index.html` defines hero/outpost fallback art and optional character and
  screenshot galleries.
- `styles.css` contains the base responsive layout.
- `art-direction.css` adds the refreshed visual identity and image-first cards.
- `scripts/game-art.js` loads only local paths in `assets/official/media.json`,
  verifies each image can load, then updates the page. It never loads external
  image sources or invents artwork.
- Missing images leave the original concept art in place. Character and
  screenshot sections stay hidden until corresponding real images are present.
- `tools/import_game_assets.py` stages real images from an authorized checkout;
  it does **not** access GitHub or require a token.

The site is intended for `https://spaceatom-game.github.io/` after merging
into the upstream `main` branch.
