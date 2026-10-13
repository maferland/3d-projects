# Gridfinity cutlery tray

Adaptation of Curious Mint's [Compact Cutlery Tray](https://makerworld.com/en/models/20756-compact-cutlery-tray).
The assembled tray occupies 3 x 10 Gridfinity cells at 42 mm pitch.
Each half has 15 feet arranged 3 x 5, with the original diagonal joint and side clips.
The overlapping bodies extend beyond the five-row base footprint.

## Print files

These STLs and the rendered joint images are local artifacts excluded from
the public repository. The build scripts generate them from author-supplied meshes.

- `build/compact_cutlery_tray_3x10_inverted_dividers_A.stl`: existing printed A, with the undivided front bucket.
- `build/compact_cutlery_tray_B_original_clips_v3.stl`: corrected B; print this to mate with the existing A. The original side clips are protected from the repair cuts.
- `build/compact_cutlery_tray_3x10_inverted_dividers_B.stl`: previous B, retained only as the input for generating the receiver correction. Do not print this version.

A measures 125.5 x 230.94 x 61.6 mm. Revised B measures 125.5 x 230.69 x 61.6 mm.
B's receiver provides 0.25 mm clearance around A's added divider and backing
geometry, with 0.05 mm contact relief limited to those repair regions. Both
original clip regions are protected. A remains unchanged.

## Verification

The exported revised B is watertight and Bambu Studio reports it manifold.
Boolean intersection between the saved A and revised B is below 0.001 mm3,
consistent with numerical contact at the original clip surfaces. The repair
removes approximately 1,782 mm3 (0.47%) of B's material. The clip geometry is
unchanged within mesh numerical precision.
Physical fit, clip retention, and strength still require checking after printing.

`build/B_original_clips_v3_fit_report.json` records the input hashes and measurements.
The joint images show the saved A in blue and revised B in green.

## Rebuild

Use Python 3.10 or newer and Node.js. Install dependencies:

```sh
npm ci
uv venv .venv
uv pip install --python .venv/bin/python -r requirements-cutlery.txt
```

Regenerate the saved A and original B inputs from the source split meshes:

```sh
node compile_scad_with_stl.mjs remix_inverted_dividers.scad source/CutleryDrawA.stl build/compact_cutlery_tray_3x10_inverted_dividers_A.stl source_y_max=-177.544098 plate_source_y_max=-217.455933 last_foot_row=4
node compile_scad_with_stl.mjs remix_inverted_dividers.scad source/CutleryDrawB.stl build/compact_cutlery_tray_3x10_inverted_dividers_B.stl source_y_min=-217.455933 first_foot_row=5
```

To preserve compatibility with an already printed A, retain its committed STL
and use its hash in the fit report. Then generate the revised B and review images:

```sh
.venv/bin/python fit_B_to_printed_A.py
```

To use source and saved STL files in another checkout, pass that folder as the
first argument to `fit_B_to_printed_A.py`.

The other render scripts require Blender's Python runtime. They are optional.

## Source attribution

Original source meshes are in `source/`. The source model was supplied under
CC BY-NC-ND; do not publicly redistribute modified meshes without the author's
permission. No broader license is granted to those source meshes here.

The separate Elumara project is documented in `README.elumara.md`.
