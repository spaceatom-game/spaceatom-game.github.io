#!/usr/bin/env python3
"""Copy original SpaceAtom artwork from an authorized local game checkout."""
from __future__ import annotations
import argparse
import json
import re
import shutil
from pathlib import Path

FORMATS = {".png", ".jpg", ".jpeg", ".webp", ".svg"}
SKIP_PARTS = {".godot", ".git", "addons", "imported", "cache", "third_party"}
TARGET = Path("assets/official")
WORDS = {
    "logo": ("logo", "wordmark", "game_title", "spaceatom_title"),
    "hero": ("key_art", "keyart", "cover", "hero", "banner", "screenshot"),
    "ally": ("ally_outpost", "ally_post", "friendly_outpost", "allied_outpost"),
    "enemy": ("enemy_outpost", "enemy_post", "hostile_outpost"),
}

def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:60] or "image"

def images(root: Path) -> list[Path]:
    return sorted(
        (p for p in root.rglob("*") if p.is_file()
         and p.suffix.lower() in FORMATS and not SKIP_PARTS.intersection(p.parts)),
        key=lambda p: str(p).lower(),
    )

def suggested(items: list[Path], kind: str) -> Path | None:
    choices = []
    for p in items:
        stem = p.stem.lower()
        rel = str(p).lower()
        score = sum(10 if term in stem else 1 for term in WORDS[kind] if term in rel)
        if kind in {"ally", "enemy"} and "outpost" in rel:
            score += 6 if score else 0
        if score:
            choices.append((score, str(p), p))
    return max(choices, default=(0, "", None))[2]

def source_file(root: Path, raw: str) -> Path:
    value = Path(raw)
    path = (value if value.is_absolute() else root / value).resolve()
    if not path.is_relative_to(root) or not path.is_file() or path.suffix.lower() not in FORMATS:
        raise ValueError(f"Not a supported image inside the game checkout: {raw}")
    return path

def stage(path: Path, name: str, site: Path, dry_run: bool) -> str:
    dst = TARGET / (slug(name) + path.suffix.lower())
    print(f"  {path} -> {site / dst}")
    if not dry_run:
        (site / TARGET).mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, site / dst)
    return "./" + dst.as_posix()

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--game-root", type=Path, required=True,
                        help="Authorized local checkout of the SpaceAtom game")
    parser.add_argument("--site-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--logo", help="Path relative to the game checkout")
    parser.add_argument("--hero", help="Path relative to the game checkout")
    parser.add_argument("--ally", help="Path relative to the game checkout")
    parser.add_argument("--enemy", help="Path relative to the game checkout")
    parser.add_argument("--character", action="append", default=[], metavar="NAME=PATH")
    parser.add_argument("--screenshot", action="append", default=[], metavar="PATH")
    parser.add_argument("--no-auto", action="store_true",
                        help="Select only explicitly provided files")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview selections without copying or changing the manifest")
    args = parser.parse_args()
    game = args.game_root.resolve()
    site = args.site_root.resolve()
    if not game.is_dir():
        parser.error("--game-root does not exist")
    if not (site / "index.html").is_file():
        parser.error("--site-root must contain index.html")
    source_images = [] if args.no_auto else images(game)
    print(f"Found {len(source_images)} candidate images.")
    manifest = {"version": 1, "logo": None, "hero": None, "ally": None,
                "enemy": None, "characters": [], "screenshots": []}
    for key in WORDS:
        raw = getattr(args, key)
        chosen = source_file(game, raw) if raw else suggested(source_images, key)
        if chosen:
            manifest[key] = stage(chosen, key, site, args.dry_run)
        else:
            print(f"  No {key} artwork selected; site keeps its existing fallback.")
    for number, value in enumerate(args.character[:12], start=1):
        if "=" not in value:
            parser.error(f"Expected --character NAME=PATH; got {value}")
        name, path = value.split("=", 1)
        if not name.strip():
            parser.error("Character name must not be blank")
        asset = stage(source_file(game, path), f"character-{number:02}-{name}", site, args.dry_run)
        manifest["characters"].append({
            "name": name.strip(), "role": f"FILE // {number:02}", "image": asset})
    for number, path in enumerate(args.screenshot[:8], start=1):
        asset = stage(source_file(game, path), f"screenshot-{number:02}", site, args.dry_run)
        manifest["screenshots"].append({
            "image": asset, "caption": f"GAME CAPTURE // {number:02}"})
    dest = site / TARGET / "media.json"
    if args.dry_run:
        print(json.dumps(manifest, indent=2))
    else:
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        print(f"Created {dest}. Verify every image and licensing before publishing.")

if __name__ == "__main__":
    main()
