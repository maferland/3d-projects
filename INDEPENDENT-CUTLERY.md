# Independent angled cutlery tray — prototype

Constructed from geometric primitives without importing the earlier tray meshes.
The assembled footprint is 125.5 x 419.5 mm (3 x 10 Gridfinity cells).
Each half has five rows of three feet and a continuous supporting floor.
The first upper pocket is undivided; its under-slope tunnel is divided.
The other three pockets have center dividers.

The shell, slopes, floor, and dividers are split together with one diagonal
interface and a 0.3 mm longitudinal gap. Two separate bow-tie locking keys
drop into recesses at the rim to hold the halves together. Each key has
0.25 mm clearance from its socket walls. The keys are removable friction-fit
parts; this prototype does not use spring snap clips.

Print the joint coupons and two keys before the full halves. Check insertion,
key retention, rigidity, print orientation, and support needs. Coupons are
cropped copies of the full joint, including the center divider and both rim
sockets. After testing, print A and B and two keys. This pair is a new design
and is not intended to mate with the previous adapted A.

## Build and verification

```sh
npm ci
node export-independent.mjs A
node export-independent.mjs B
node export-independent.mjs key
node export-independent.mjs coupon_A
node export-independent.mjs coupon_B
uv venv .venv
uv pip install --python .venv/bin/python -r requirements-cutlery.txt
.venv/bin/python verify-independent.py
.venv/bin/python render-independent.py
```

Exports, inspection renders, and the verification report appear in
`independent-exports/`. Mesh collision checks cover the assembled halves,
both keys, and several positions along the straight assembly path. These
checks do not establish physical fit, utensil capacity, print quality, or
material strength. This prototype needs physical testing before a MakerWorld
print profile is published.
