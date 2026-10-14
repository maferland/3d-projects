# Lessons from the cutlery tray project

The task was to fit an existing angled cutlery tray to a 3 x 10 Gridfinity
footprint, change its dividers, and preserve the original male/female joint.
One half had already been printed. The rules in [AGENTS.md](../AGENTS.md)
generalize the lessons below to future 3D projects.

## Preserve the user's chosen mechanism

We replaced the selected tray with an independent design and substituted
drop-in keys, then a different spring clip. Those changes solved different
problems than the one requested. The keys also added inward rim shoulders
that could snag cutlery. The accepted correction returned to the saved tray
and protected its original connector regions while repairing divider clearance.

Lesson: ask before changing the model or mechanism. Show the tradeoff in
usable space, compatibility, and printing before implementing a redesign.

## Grid footprint and body length are different

The original joint overlapped longitudinally. Demanding an exact five-cell
bounding length for each half led to a flat cut through a sloped pocket,
removed the diagonal joint, and produced a thin edge. Preserving five foot
rows per half allowed the body overlap while retaining ten installed rows.

Lesson: report foot occupancy, body bounds, and bed fit separately.

## A divider must work above, below, and across the joint

An estimated slope left a gap under a divider against the imported curved
floor. Extending the wrong end created a block in the neighboring pocket.
Later, a divider that looked complete above the tray still left its hidden
under-basket tunnel open. Extending it then blocked assembly because both
halves occupied the same space in the joint.

Lesson: inspect the entire cutlery path and the complete assembled pair.
Added material must join the floor and also respect mating clearance.

## Backing and receiver clearance are asymmetric

A continuous backing plate filled the female receiving region, making both
halves appear to have male tongues. Removing backing from both halves then
left B's nearest Gridfinity row partially unsupported. The pair needed female
clearance on A and continuous supporting material beneath B's tongue.

Lesson: evaluate support and clearance together; symmetry is not always correct.

## Mesh health is only one layer of evidence

Repeated manifold checks passed while physical concerns remained visible.
An overview hid divider ends; a single ray check missed a groove elsewhere
in the pocket. Close views exposed the channel and its terminal dimple.

The final original-model correction preserved the saved A byte-for-byte.
Measured pair overlap fell from roughly 1,020 mm3 to less than 0.001 mm3;
the protected clip regions changed only within numerical mesh precision.
This establishes computational clearance, not physical clip retention or
utensil capacity. Physical testing remains necessary.

Lesson: combine mesh checks, region comparisons, collision checks, assembly
views, cutaways, underside inspection, slicer import, and physical fit tests.

## Clear handoff prevents wasted prints

Full halves, cropped coupons, older candidates, and different mechanisms
accumulated under similar filenames. The user had to ask for the full-size
files and discover connector changes during testing.

Lesson: version the pair, label its mechanism, link full files explicitly,
identify which existing part remains compatible, and state what to reprint.
Keep prototype geometry and untested platform profiles clearly marked.
