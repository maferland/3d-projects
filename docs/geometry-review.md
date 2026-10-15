# Geometry review

Select checks that can expose the reported defect. Use the actual exported
files and assembled coordinate system. A documentation change does not need
a full CAD rebuild; an edit to a mating surface does need a mating check.

## 1. State what success means

Before editing, record:

- Reference model/version and hashes of any files corresponding to printed parts.
- Allowed changes, protected geometry, and compatibility/reprint constraints.
- Separate dimensions for installed footprint, foot rows, body overlap, and bed fit.
- Assembly direction, intended interference/flex, and process-specific clearance.
- A measurable criterion for the defect, plus checks for nearby regressions.

If constraints conflict, expose the conflict before choosing which to relax.

## 2. Choose evidence for the failure

| Failure or change | Required evidence | What it does not establish |
| --- | --- | --- |
| Split or mating repair | Pair intersection, protected-region difference, and samples along assembly motion | Clip flex, wear, or retention |
| Added divider | Close root/tip views, tunnel cutaway, floor contact, and assembled mate clearance | Actual utensil capacity |
| Removed divider or floor patch | Entire-pocket inspection and surface measurements across the former feature and attachments | A single cross-section cannot establish a smooth pocket |
| Backing or foot change | Underside view, connected material, and support beneath every affected foot | Grid fit in a physical drawer |
| Footprint or size change | Reloaded dimensions, grid occupancy, and printer build volume | An overlapping body need not have the same length as its base |
| Connector change | User agreement, clearance checks, usable-space comparison, and a faithful test coupon | A different connector is not automatically a better repair |
| Model publication | Source/permission record, reproducible files, clear validation status | Slicer acceptance is not a tested print profile |

Check watertightness, orientation, and unexpected material components when
exporting changed geometry. Multiple surface shells may represent internal
cavities; inspect them before filling holes or deleting components.

Compare views from the same camera direction. For suspected render artifacts,
measure the relevant surface over the whole affected region. Do not dismiss a
visible defect as shading from an overview or one ray sample.

## 3. Interpret numerical results honestly

- Record clearance, collision residual, protected-region change, and tolerances.
  Choose tolerances for the model scale and process; do not treat one project's
  threshold as universal. Compare with original-model contact when useful.
- Separate seated overlap from intended insertion contact. Localizing contact
  to a spring tooth is a diagnostic, not a mechanical simulation.
- A new union must have finite overlap where strength is required. A mathematical
  point contributes negligible connection; coincident-only joins and zero-area
  faces can produce fragile or invalid output.
- Preserve curved floor geometry or derive the join from the actual mesh.
  A linear approximation can be correct at one point and leave a gap elsewhere.
- For an existing mechanism, keep repairs outside its protected region. Consider
  asymmetric backing before removing support from both halves.

## 4. Handoff

State the selected version, full-size file links, matching pair, mechanism,
existing-part compatibility, required reprints, checks passed, and remaining
physical checks. Provide coupons when they exercise the real interface.

Before a tested model-platform release, record the printer, nozzle, material,
settings, orientation/supports, fit results, and photographs. Include actual
utensil/load tests where those are part of the design requirements.
