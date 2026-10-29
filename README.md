# SpaceAtom pitch website

A responsive, static landing page that introduces **SpaceAtom**, an independent space-action game being developed in Godot.

## Site content

- A game overview and an easy-to-follow description of the intended experience.
- A visual explanation of the ally and enemy outposts.
- The solo-development story and Android-first release goal.
- Links to the project organization and developer.
- Original SVG **concept illustrations** (clearly marked as concepts, not gameplay screenshots).

## Local preview

No dependencies, build tools, or JavaScript framework are required.

```sh
python3 -m http.server 8000
```

Open http://localhost:8000.

## Deploying with GitHub Pages

The repository is intended to serve the site from the root of the `main` branch as `https://spaceatom-game.github.io/` after the pull request is merged and GitHub Pages has been enabled under **Settings → Pages** (Deploy from a branch; `main` / `/ (root)`).

## Updating content

- `index.html` — copy, semantic structure, SEO information, and links.
- `styles.css` — styling and responsive layouts.
- `assets/hero-scene.svg` — original hero illustration.
- `assets/outpost-ally.svg` and `assets/outpost-enemy.svg` — illustrative outpost art.
- `assets/favicon.svg` — site icon.

**Important:** The source game assets and current playable build were not accessible when this initial website was authored. The illustrations are **not** exported screenshots or canon game artwork. Replace or supplement them with approved in-game assets as they become available, and review the descriptions when mechanics are finalized.
