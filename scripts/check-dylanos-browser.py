#!/usr/bin/env python3
"""Validate DylanOS Browser branding and preference contracts without building Firefox."""
from __future__ import annotations
import json
import re
import struct
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")
    print(f"OK: {message}")

def pref_values(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    current = None
    for line in path.read_text(encoding="utf-8").splitlines():
        name = re.match(r"\s*-\s*name:\s*([\w.-]+)\s*$", line)
        if name:
            current = name.group(1)
            continue
        value = re.match(r"\s+value:\s*(\"[^\"]*\"|\'[^\']*\'|[^#\s]+)", line)
        if current and value:
            values[current] = value.group(1).strip('"\'')
            current = None
    return values

meta = json.loads((ROOT / "surfer.json").read_text(encoding="utf-8"))
require(meta.get("name") == "DylanOS Browser", "product name")
require(meta.get("appId") == "dylanos-browser", "unique app ID")
require(meta.get("license", {}).get("licenseType") == "MPL-2.0", "MPL-2.0 metadata preserved")
for channel in ("release", "twilight"):
    brand = meta["brands"][channel]
    require(brand["brandFullName"].startswith("DylanOS Browser"), f"{channel} channel brand")
    require(brand["release"]["github"]["repo"] == "CRISTOP-bot/DylanOS-Browser", f"{channel} fork update/build repo")
    require(brand["backgroundColor"].lower() == "#110d13", f"{channel} Crimson dark background")

browser = pref_values(ROOT / "prefs/firefox/browser.yaml")
theme = pref_values(ROOT / "prefs/zen/theme.yaml")
for key in ("browser.profiles.enabled", "browser.tabs.groups.enabled", "browser.tabs.splitView.enabled"):
    require(browser.get(key) == "true", f"new-profile feature enabled: {key}")
require(browser.get("browser.sessionstore.interval") == "30000", "session save cadence")
require(theme.get("zen.theme.accent-color", "").upper() == "#DC143C", "DylanOS Crimson browser accent")
security = pref_values(ROOT / "prefs/firefox/extensions.yaml")
require(security.get("xpinstall.signatures.required") == "true", "signed extension requirement stays enabled")

license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
require("Mozilla Public License Version 2.0" in license_text, "upstream MPL text retained")
require("MPL 2.0" in (ROOT / "DYLANOS-BROWSER.md").read_text(encoding="utf-8"), "fork license/source notes present")

for channel in ("release", "twilight"):
    for size in (16, 22, 24, 32, 48, 64, 128, 256, 512, 1024):
        path = ROOT / f"configs/branding/{channel}/logo{size}.png"
        data = path.read_bytes()
        require(data[:8] == b"\x89PNG\r\n\x1a\n", f"{channel} {size}px icon PNG")
        width, height = struct.unpack(">II", data[16:24])
        require((width, height) == (size, size), f"{channel} icon dimensions {size}x{size}")
for name in ("about-logo.svg", "about-logo-private.svg", "about-wordmark.svg"):
    ET.parse(ROOT / "configs/branding/release/content" / name)
    require(True, f"well-formed release SVG: {name}")
print("Source branding checks passed. These checks do not compile or run the browser.")
