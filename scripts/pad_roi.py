#!/usr/bin/env python3
"""Measure the ten emissive SLAB pads at projected regions of interest.

Diagnostic measurement only - it builds nothing and decides nothing about the
model. It replaces colour-threshold blob counting for the pad acceptance test:
thresholds also catch the orange large knobs, highlights and the power LED.

Workflow (after the raytrace has finished - execute_code blocks during one):
  1. In Fusion, project each Keypad body's top-centre with
     app.activeViewport.modelToViewSpace(Point3D) and write
     {"vp": [viewport_w, viewport_h], "pads": [[x, y], ...]} to a JSON file.
  2. python scripts/pad_roi.py render.png rois.json
The render must use view='current' with the same camera, so image pixels are
viewport pixels scaled by image_height / viewport_height (the aspect matches
when sceneSettings.aspectRatio is CurrentViewport).

Acceptance (slab-run): mean G:R 0.55 +/- 0.03, mean luminance 144..160.5,
per-channel spread across the ten pads <= 7 levels.
"""
import argparse
import json
import sys

import numpy as np
from PIL import Image

LUMW = np.array([0.2126, 0.7152, 0.0722])


def measure(img, rois, roi_half_vp_px=5.0):
    """Return a dict of pad metrics. img: HxWx3 array, rois: dict from JSON."""
    img = np.asarray(img, dtype=np.float32)
    h, w = img.shape[:2]
    vw, vh = rois["vp"]
    s = h / float(vh)
    if abs(w / float(h) - vw / float(vh)) > 0.01:
        raise ValueError(f"image aspect {w}x{h} does not match viewport {vw}x{vh}; "
                         "render with aspectRatio=CurrentViewport or re-project")
    pads = rois["pads"]
    if len(pads) != 10:
        raise ValueError(f"expected 10 pad ROIs, got {len(pads)}")
    rad = max(2, int(round(roi_half_vp_px * s)))
    means = []
    for x, y in pads:
        cx, cy = int(round(x * s)), int(round(y * s))
        if not (rad <= cx < w - rad and rad <= cy < h - rad):
            raise ValueError(f"ROI ({cx},{cy}) falls outside the {w}x{h} frame")
        patch = img[cy - rad:cy + rad + 1, cx - rad:cx + rad + 1].reshape(-1, 3)
        means.append(np.median(patch, axis=0))
    m = np.array(means)
    lum = m @ LUMW
    gr = m[:, 1] / np.maximum(m[:, 0], 1e-6)
    spread = m.max(axis=0) - m.min(axis=0)
    res = {
        "size": [w, h], "roi_half_px": rad,
        "rgb_mean": [round(float(v), 1) for v in m.mean(axis=0)],
        "lum_mean": round(float(lum.mean()), 1),
        "lum_range": [round(float(lum.min()), 1), round(float(lum.max()), 1)],
        "gr_mean": round(float(gr.mean()), 3),
        "spread": [round(float(v), 1) for v in spread],
        "red_clipped": bool(m[:, 0].min() >= 254.0),
    }
    res["pass_gr"] = abs(res["gr_mean"] - 0.55) <= 0.03
    res["pass_lum"] = 144.0 <= res["lum_mean"] <= 160.5
    res["pass_spread"] = max(res["spread"]) <= 7.0
    return res


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("img")
    ap.add_argument("rois")
    ap.add_argument("--roi", type=float, default=5.0,
                    help="ROI half-size in viewport pixels (default 5)")
    a = ap.parse_args(argv)
    img = np.asarray(Image.open(a.img).convert("RGB"))
    res = measure(img, json.load(open(a.rois, encoding="utf-8")), a.roi)
    verdict = lambda ok: "PASS" if ok else "FAIL"
    print(f"{a.img}: {res['size'][0]}x{res['size'][1]} roi+/-{res['roi_half_px']}px "
          f"rgb {res['rgb_mean']} lum {res['lum_mean']} {res['lum_range']} "
          f"G:R {res['gr_mean']} spread {res['spread']}"
          f"{' RED CLIPPED' if res['red_clipped'] else ''} -> "
          f"G:R {verdict(res['pass_gr'])} lum {verdict(res['pass_lum'])} "
          f"spread {verdict(res['pass_spread'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
