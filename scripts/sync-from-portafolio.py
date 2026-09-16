#!/usr/bin/env python3
"""Sync data from portafolio/src/data/* -> pablov01/assets/*.json + regenerate svgs.
Usage: python scripts/sync-from-portafolio.py [--portafolio PATH]
"""
import argparse, json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PORTAFOLIO = ROOT.parent / "portafolio"

def extract_ts_object(text: str, const_name: str):
    # naive: find "export const NAME = { ... };" and extract JSON-ish
    m = re.search(rf"export const {const_name}\s*=\s*\{{(.*?)\n\}}", text, re.S)
    if not m: return None
    # not used — we parse manually below
    return m.group(0)

def parse_skills(portafolio: Path):
    src = (portafolio / "src/data/profile.ts").read_text()
    # extract SKILLS_RADAR axes
    def parse_radar(name):
        block = re.search(rf"export const {name}\s*=\s*\{{.*?axes:\s*\[(.*?)\]", src, re.S)
        if not block: return []
        axes_txt = block.group(1)
        axes = re.findall(r'\{\s*label:\s*"([^"]+)"\s*,\s*value:\s*(\d+)', axes_txt)
        title_m = re.search(rf"export const {name}\s*=\s*\{{\s*title:\s*\"([^\"]+)\"", src)
        title = title_m.group(1) if title_m else name
        return title, [{"label": l, "value": int(v)} for l, v in axes]
    skills_title, skills_axes = parse_radar("SKILLS_RADAR")
    stack_title, stack_axes = parse_radar("STACK_RADAR")
    return (skills_title, skills_axes), (stack_title, stack_axes)

def parse_projects(portafolio: Path):
    src = (portafolio / "src/data/projects.ts").read_text()
    repos = re.findall(r'repo:\s*"([^"]+)"', src)
    # descriptions: capture repo + description pairs
    descs = re.findall(r'repo:\s*"([^"]+)"\s*,\s*title:[^,]+,\s*description:\s*"([^"]+)"', src, re.S)
    # fallback: map repo->desc
    desc_map = {r: d for r, d in descs}
    return repos, desc_map

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--portafolio", type=Path, default=DEFAULT_PORTAFOLIO)
    args = ap.parse_args()
    portafolio = args.portafolio
    if not (portafolio / "src/data/profile.ts").exists():
        print(f"portafolio not found at {portafolio}", file=sys.stderr)
        sys.exit(1)

    (skills_title, skills_axes), (stack_title, stack_axes) = parse_skills(portafolio)
    repos, desc_map = parse_projects(portafolio)

    assets = ROOT / "assets"
    assets.mkdir(parents=True, exist_ok=True)

    (assets / "skills.json").write_text(json.dumps({"title": skills_title, "axes": skills_axes}, indent=2, ensure_ascii=False) + "\n")
    (assets / "stack.json").write_text(json.dumps({"title": stack_title, "axes": stack_axes}, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote skills.json ({len(skills_axes)} axes) + stack.json ({len(stack_axes)} axes)")

    # projects.json — only repos that exist on GitHub will get cards; include up to 4
    projects = []
    for r in repos[:4]:
        projects.append({"repo": r, "description": desc_map.get(r, "")})
    (assets / "projects.json").write_text(json.dumps({"_comment": "Sync from portafolio/src/data/projects.ts", "projects": projects}, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote projects.json ({len(projects)} repos: {', '.join(repos[:4])})")

    # regenerate
    for cmd in [
        ["python3", "scripts/radar.py", "--data", "assets/skills.json", "-o", "assets/radar"],
        ["python3", "scripts/radar.py", "--data", "assets/stack.json", "-o", "assets/radar-stack", "--values"],
        ["python3", "scripts/generate-banner.py"],
    ]:
        print(f"$ {' '.join(cmd)}")
        subprocess.run(cmd, cwd=ROOT, check=False)
    # cards needs token; try without
    print("$ python3 scripts/cards.py --user pablov01 --out assets")
    subprocess.run(["python3", "scripts/cards.py", "--user", "pablov01", "--out", "assets"], cwd=ROOT, check=False)
    print("done — commit assets/*.svg + *.json")

if __name__ == "__main__":
    main()
