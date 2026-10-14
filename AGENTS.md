# Working on 3D projects

These instructions apply to CAD sources, mesh edits, printable exports, and
publication assets in this repository. See [project lessons](docs/3d-project-lessons.md)
for the failures that motivated them.

## Establish the design contract

- Record the selected model, dimensions in millimeters, grid pitch, compartment
  layout, mating mechanism, printer limits, and intended publication target.
- Preserve accepted geometry and mechanisms by default. Ask before replacing
  a model, changing its split, substituting a connector, or moving a feature
  into usable storage space. Permission to fix a defect is not blanket
  permission to redesign the object.
- If a part is already printed, identify its source STL and save its hash.
  Treat that geometry as fixed. Prefer repairing its mate when the fit and
  strength allow it; explain the evidence if both parts need reprinting.
- Inspect the current branch and local changes before editing. Use a task
  branch/worktree under `.worktrees/` with the `maferland/` prefix. Preserve
  unrelated files. Use `rtk`, or `rtk proxy` for raw command output.

## Edit geometry with its mating parts in view

- Inspect original parts together in their assembled coordinates before
  modifying them. Identify male/female features, overlap, assembly direction,
  flexible regions, and protected surfaces. Different camera directions can
  make a diagonal appear reversed; compare identical views.
- Separate grid occupancy, foot rows, body bounds, and print-bed bounds.
  An overlapping body can be longer than its grid base without consuming
  another grid row. Never flatten a proven joint just to meet a bounding box.
- Carry dividers through hidden under-shelf tunnels. Check both root and tip.
  Split or relieve added dividers to match the mating interface; meeting the
  visible cross-wall does not prove utensils are separated underneath it.
- Use the actual floor geometry when joining a divider. An estimated straight
  slope can leave gaps against a curved floor. Overlap and union added material
  deliberately, while protecting cavities and mating clearance.
- Keep backing connected to every Gridfinity foot. Support can be asymmetric:
  a female receiver needs clearance while its mate needs a supported tongue.
  Check both halves together after changing either one's backing.
- Remove a feature through its attachment regions as well as its visible body.
  A short floor patch can leave a groove or terminal dimple. Avoid zero-area
  tips and coincident-only joins; use finite contact and a valid solid.

## Verify the requested behavior

- Reload the exported STL and check dimensions, watertightness, normals,
  connected material, and unexpected shells. Cavity boundaries are not
  necessarily detached material; inspect them before making changes.
- Check Boolean overlap of the assembled exported pair. Protect original
  connector regions and quantify any geometry changes there. Record tolerance
  and residual overlap rather than calling a small nonzero result exactly zero.
- Check the assembly path too. Intended spring-tooth contact during insertion
  is different from rigid divider interference. A contact test alone does not
  prove a clip can flex safely, retain the parts, or survive repeated use.
- Render the assembled object, separated joint, close side/top views, center
  cutaway, and underside as relevant to the defect. Use the actual exported
  meshes. A distant overview or one ray sample cannot prove a pocket is smooth.
- Treat a suspected shading seam as unproven until geometry measurements across
  the affected region establish whether it is a real groove or protrusion.
- Import final exports into the target slicer when available. Manifoldness
  alone does not prove mating fit, utensil clearance, support removal, strength,
  or printability. Report computational and physical validation separately.
- Offer a small joint coupon before a full reprint when it faithfully exercises
  the proposed fit. Do not claim a MakerWorld print profile is tested without
  a physical print and the recorded printer/material/settings.

## Deliver unambiguous, reproducible files

- Give each candidate a clear version and mechanism label. Keep full halves,
  coupons, and connector-only parts distinguishable. Link the full-size files
  directly in the handoff; say which pair belongs together and what to reprint.
- Preserve files corresponding to existing prints. Do not silently replace
  their baselines or mix files from different designs.
- Pin build dependencies and use project-relative imports. Avoid build scripts
  depending on temporary runtime locations. Save generation parameters, input
  hashes, and verification results so a later session can reproduce the export.
- Keep repository publication and model-platform publication separate. Check
  source provenance, applicable license, permission, and attribution before
  publishing meshes. An independent redesign is a separate design decision
  requiring user agreement; a public repo does not override source restrictions.
- Never silently publish an abandoned prototype as the selected final model.
  State remaining physical checks and keep drafts clearly labeled.
