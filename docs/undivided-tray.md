# Undivided tray variant

This optional variant removes the center dividers from the three previously
split sections, including their hidden tunnel portions. The front pocket stays
undivided. Basket slopes, original male/female clips, installed 3 x 10 footprint,
and five Gridfinity foot rows per half are retained.

Use the new A/B pair together. To obtain the completely undivided layout,
both halves need printing; the previous divided files remain available.
Physical fit and utensil capacity still require testing.

## Generate from the local original source files

Run from the repository root after installing the documented dependencies:

```sh
mkdir -p build/undivided-original-clips
node compile_scad_with_stl.mjs remix_inverted_dividers.scad source/CutleryDrawA.stl build/undivided-original-clips/cutlery_A.stl source_y_max=-177.544098 plate_source_y_max=-217.455933 last_foot_row=4 include_dividers=false
node compile_scad_with_stl.mjs remix_inverted_dividers.scad source/CutleryDrawB.stl build/undivided-original-clips/raw_B.stl source_y_min=-217.455933 first_foot_row=5 include_dividers=false
.venv/bin/python fit_B_to_printed_A.py . --part-a build/undivided-original-clips/cutlery_A.stl --part-b build/undivided-original-clips/raw_B.stl --output build/undivided-original-clips/cutlery_B.stl --report build/undivided-original-clips/verification.json
```

Print `cutlery_A.stl` and `cutlery_B.stl`. `raw_B.stl` is a build input before
backing-clearance correction, not a print candidate. The fit report records
the reference A hash, pair overlap, and protected clip-region comparison.
The source and derived meshes remain excluded from the public repository.

`include_dividers` defaults to `true`, preserving the divided build option.
The optional fit-script paths select this variant without replacing the saved
printed-A baseline or the divided version's reports.
