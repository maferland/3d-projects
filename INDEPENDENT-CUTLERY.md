# Independent angled cutlery tray — prototype

Constructed from geometric primitives without importing the earlier tray meshes.
The assembled footprint is 125.5 x 419.5 mm (3 x 10 Gridfinity cells).
Each half has five rows of three feet and a continuous supporting floor.
The first upper pocket is undivided; its under-slope tunnel is divided.
The other three pockets have center dividers.

The shell, slopes, floor, and dividers are split together with one diagonal
interface and a 0.3 mm longitudinal gap. Two integrated spring clips on B fit
recesses in A's outer wall. The tabs and receivers remain within the 125.5 mm
width and add no inward shoulder to the cutlery openings. The tabs are 1.1 mm
thick and require about 0.2 mm outward flex at the entry lip before seating.

Print the joint coupons before the full halves. Check insertion,
clip retention, rigidity, print orientation, and support needs. Coupons are
cropped copies of the full joint, including the center divider and both outside
clips. After testing, print A and B. This pair is a new design
and is not intended to mate with the previous adapted A.

## Build and verification

```sh
npm ci
node export-independent.mjs A
node export-independent.mjs B
node export-independent.mjs coupon_A
node export-independent.mjs coupon_B
uv venv .venv
uv pip install --python .venv/bin/python -r requirements-cutlery.txt
.venv/bin/python verify-independent.py
.venv/bin/python render-independent.py
```

Exports, inspection renders, and the verification report appear in
`independent-exports/`. Mesh collision checks cover the assembled halves,
and the assembly path at 1 mm increments. Seated halves have zero collision;
insertion contact is confined to the flexible clip teeth. These
checks do not establish physical fit, utensil capacity, print quality, or
material strength. This prototype needs physical testing before a MakerWorld
print profile is published.
