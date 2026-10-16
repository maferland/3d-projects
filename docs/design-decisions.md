# Accepted design decisions

This records user choices, not assumptions for all future projects. Update it
when the user changes direction. Historical alternatives stay in Git history;
their presence on a branch does not make them approved designs.

## Cutlery tray

### Selected design

Preserve the previous tray adaptation and its original male/female diagonal
clips. Correct the divider interference while retaining basket layout and
Gridfinity support. The installed footprint is 3 x 10 cells; each half has
3 x 5 feet. Body overlap is permitted and measured separately from occupancy.

The reference A has already been printed. Preserve it byte-for-byte:

```text
f2361a2681afe502c3f7ab6871ff529136e2c1172609e60965b838dc3ebf1b01
```

Local artifacts, relative to the working repository:

```text
build/original-tray-clip-fit/cutlery_A.stl
build/original-tray-clip-fit/cutlery_B.stl
```

They are excluded from the public repository. The correction is implemented
by `fit_B_to_printed_A.py`; its recorded measurements are in
[the v3 fit report](../build/B_original_clips_v3_fit_report.json).
Retain the original saved A/B inputs to reproduce it.

### Validation status

The recorded export checks establish watertightness, slicer import, removal
of the large divider collision, and preservation of the original clip regions
within numerical precision. They do not establish physical assembly, clip
retention, strength, or capacity for the user's actual utensils.

The next physical step is to test corrected B against the saved printed A.
There is no reason established by the current geometry checks to reprint A.

### Additional accepted variant

The user also requested an undivided version of the three split sections.
This retains the selected baskets, original clips, and Gridfinity base while
omitting added center walls above and beneath the slopes. It is a separate
matching A/B pair; the saved printed A and divided pair remain unchanged.
See [undivided tray](undivided-tray.md) for generation and print filenames.

### Superseded alternatives

The independent design with drop-in rim keys and its later replacement spring
clips were rejected in favor of the previous model and original mechanism.
They remain on `maferland/independent-cutlery` as historical experiments.
Do not merge their STLs, build instructions, or publication draft into the
selected design without a new user decision.

### Publication

MakerWorld remains the intended destination. The existing repository records
source redistribution restrictions; a model upload remains conditional on
applicable permission and physical validation. Do not silently substitute an
independent design to resolve a publication constraint.
