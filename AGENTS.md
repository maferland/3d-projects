# Working on 3D projects

## Before changing geometry

- Read the project's README and [accepted design decisions](docs/design-decisions.md).
  Record the defect, selected reference, dimensions, protected features, and
  observable acceptance criteria. Reuse established decisions; ask only when
  a missing choice or conflict would materially change the result.
- Preserve the accepted model, mechanism, and usable space. Replacing a joint
  or redesigning the object needs agreement; permission to repair a defect
  does not authorize those substitutions.
- Treat an already printed part as a fixed interface: identify the STL/hash,
  modify its mate when viable, and explain why if both need reprinting.
- Inspect branch and local changes. Use a `maferland/` task branch/worktree
  under `.worktrees/`, preserve unrelated work, and run commands through `rtk`.

## Build and verify

- Make the smallest complete repair. Scope Boolean cuts/unions explicitly;
  measure changes in protected regions rather than assuming they survived.
- Check the object as a system: mates, assembly motion, hidden utensil paths,
  foot backing, print-bed bounds, and occupied grid cells are separate concerns.
  Do not solve one by silently violating another.
- Use [geometry review](docs/geometry-review.md) to select checks relevant to
  the defect. Inspect the reloaded exports. A manifold mesh or attractive render
  alone is insufficient evidence of fit. Do not repeat checks without a new
  change, failure, or unresolved concern.
- Distinguish measured clearance, simulated/contact behavior, slicer import,
  and physical print validation. State tolerances, residuals, and limitations.
  Never describe untested clip retention or strength as verified.

## Deliver and retain knowledge

- Version matching pairs; distinguish full parts, coupons, and prototypes.
  Link full files directly and state compatibility and required reprints.
  Preserve baselines for existing prints and mark superseded designs clearly.
- Pin dependencies; use project-relative imports. Save generation parameters,
  input hashes, and a verification report alongside deliverable versions.
- Check provenance and publication permissions before uploading meshes. Keep
  repository changes, experimental branches, and platform releases distinct.
  Never merge a rejected design as the selected model.
- Capture a lesson only when it adds a reusable decision or check: trigger,
  action, and observable evidence. Put accepted choices in the decision record,
  procedures in geometry review, and incident history in [project lessons](docs/3d-project-lessons.md).
  Avoid repeating the same rule across all three.
