# 3D projects

Personal 3D printing designs, model adaptations, and geometry verification tools.
Dimensions are in millimeters.

Agent workflow: [AGENTS.md](AGENTS.md). Design and verification lessons:
[3D project lessons](docs/3d-project-lessons.md).

## Projects

- [Gridfinity cutlery tray](README.cutlery.md): a 3 x 10 tray with angled pockets,
  original diagonal clips, and a revised B receiver compatible with an already
  printed A. Includes build scripts and collision verification.
- [Elumara mold box](README.elumara.md): ribbed printable panels for a fitted
  silicone mold box. Includes OpenSCAD source and ready-to-print panel exports.

## Cutlery source files

The cutlery project adapts Curious Mint's
[Compact Cutlery Tray](https://makerworld.com/en/models/20756-compact-cutlery-tray).
Its third-party source meshes and modified STLs remain local and are excluded
from this public repository because the source license restricts redistribution
of modifications. Obtain the original files from the author to use the scripts.

The cutlery verification report records the local input hashes and fit results.
Mesh checks do not establish physical print fit or strength.

## Dependencies

`npm ci` installs the pinned OpenSCAD WASM compiler.
Python geometry tools are pinned in `requirements-cutlery.txt`.
Blender is optional for the Blender preview scripts.
See each project's documentation for build commands and validation limits.
