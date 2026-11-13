"""Verify this edition's manifest, curriculum counts and local Markdown links."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]

def main():
    manifest = json.loads((ROOT / "PROVENANCE.json").read_text())
    failures = []
    actual = {str(path.relative_to(ROOT)) for path in ROOT.rglob("*")
              if path.is_file() and path != ROOT / "PROVENANCE.json"
              and ".git" not in path.relative_to(ROOT).parts
              and "__pycache__" not in path.relative_to(ROOT).parts
              and path.suffix not in (".pyc", ".pyo")}
    recorded = {entry["path"] for entry in manifest["files"]}
    if actual != recorded:
        failures.append(f"Manifest file-set mismatch: unrecorded={sorted(actual-recorded)}, missing={sorted(recorded-actual)}")
    for entry in manifest["files"]:
        path = ROOT / entry["path"]
        if not path.is_file():
            failures.append("Missing file: " + entry["path"])
        elif hashlib.sha256(path.read_bytes()).hexdigest() != entry["sha256"]:
            failures.append("Hash mismatch: " + entry["path"])
    base = ROOT / "curriculum/foundation-01"
    for name, key, expected in [("practice.json", "items", 40), ("labs.json", "labs", 8), ("capstones.json", "capstones", 4)]:
        rows = json.loads((base / name).read_text())[key]
        if len(rows) != expected or len({row["id"] for row in rows}) != expected:
            failures.append("Count or identifier mismatch: " + name)
    if len(list((base / "lessons").glob("*.md"))) != 8:
        failures.append("Expected eight lesson files")
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        for target in re.findall(r"\]\(([^)]+)\)", path.read_text()):
            if re.match(r"[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("#"):
                continue
            target = target.split("#", 1)[0]
            if target and not (path.parent / target).exists():
                failures.append(f"Missing local link in {path.relative_to(ROOT)}: {target}")
    if failures:
        raise SystemExit("\n".join(failures))
    print(f"Verified {len(manifest['files'])} file hashes; eight lessons, forty practice items, eight laboratories and four capstones; local Markdown links resolve.")

if __name__ == "__main__":
    main()
