import { readFile, writeFile } from "node:fs/promises";
import { createOpenSCAD } from "openscad-wasm-prebuilt";

const [scadPath, sourceStlPath, outputPath, ...overrides] = process.argv.slice(2);
if (!scadPath || !sourceStlPath || !outputPath) {
  throw new Error("Usage: node compile_scad_with_stl.mjs model.scad source.stl output.stl [name=value]");
}

let source = await readFile(scadPath, "utf8");
for (const override of overrides) {
  const separator = override.indexOf("=");
  const name = override.slice(0, separator);
  const value = override.slice(separator + 1);
  const parameterPattern = new RegExp(`^${name}\\s*=.*?;`, "m");
  if (!parameterPattern.test(source)) throw new Error(`Unknown parameter: ${name}`);
  source = source.replace(parameterPattern, `${name} = ${value};`);
}

const openscad = await createOpenSCAD({
  noInitialRun: true,
  print: (message) => console.log(message),
  printErr: (message) => console.error(message),
});
const instance = openscad.getInstance();
instance.FS.writeFile("/model.scad", source);
instance.FS.writeFile("/source.stl", await readFile(sourceStlPath));
instance.callMain(["/model.scad", "--enable=manifold", "-o", "/output.stl"]);
await writeFile(outputPath, instance.FS.readFile("/output.stl"));
