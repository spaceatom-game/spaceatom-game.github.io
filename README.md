# SpaceAtom — official game artwork website

The static pitch site for **[SpaceAtom](https://spaceatom-game.github.io/)**, a solo-developed, mobile-first space shooter built in Godot.

This website now uses **original game assets** from the private `spaceatom-game/spaceatom` repository. It presents the game's actual character portraits, app monogram, player ship vectors, boss ship, and Verdant Prime cloud background.

## Preview

```bash
python3 -m http.server 8000
```

Open <http://localhost:8000>. The site needs no build step, bundler, JavaScript framework, or access to private GitHub resources at runtime. All images used in `index.html` and `game-site.css` are committed locally.

## Authentic artwork inventory

| Website file | Source path in `spaceatom-game/spaceatom` |
| --- | --- |
| `assets/official/crew.png` | `assets/characters/crew.png` |
| `assets/official/app.svg` | `assets/icons/app.svg` |
| `assets/official/kestrel.svg` | `assets/ships/kestrel.svg` |
| `assets/official/bulwark.svg` | `assets/ships/bulwark.svg` |
| `assets/official/tempest.svg` | `assets/ships/tempest.svg` |
| `assets/official/boss.svg` | `assets/ships/boss.svg` |
| `assets/official/verdant-prime-cloud.png` | `assets/backgrounds/verdant-prime-cloud.png` |
| `assets/official/admiral-ryker.webp` | `assets/characters/admiral_ryker.webp` |

Every copied file's Git blob SHA was checked against the original source; the source PNG for `crew.png` was recovered from the **original game's embedded character SVG**, which contains an identical copy.

### Character portraits

To avoid embedding four identical 1.6 MB PNGs, the page reuses `crew.png` with inline SVG crops. The exact view boxes come from `data/catalog.json` in the game repository:

- Kai: `38 155 350 450`
- Nova: `414 155 350 450`
- Brix: `778 155 350 450`
- Zee: `1147 155 350 450`

All four use the same locally served PNG, and the crop elements are accessible via ARIA labels.

## Content notes

- The website focuses on **two playable pilots**, **three ship classes**, **four elemental worlds**, and **twelve campaign routes**, as described by the native game source.
- The hero poster is **official illustrated character art**, *not* a gameplay screenshot.
- Enemy/allied outposts are explained in prose and interface motifs. The private game's large PNG outpost images and cover illustration are not included in this first original-assets PR.
- Older experimental CSS, artwork, and image-manifest files remain in the repository for reference but **are not used by the new page**. The active entry points are `index.html` and `game-site.css`.

## Deployment

The upstream repository is `spaceatom-game/spaceatom-game.github.io`, with the public site served by GitHub Pages from the root of `main`. Changes should be made in a feature branch of `xmnlab/spaceatom-game.github.io`, based on upstream `main`, and proposed via a PR to the organization repository.

After merging, check the Pages deployment and use a hard refresh if the browser still caches the previous CSS.
