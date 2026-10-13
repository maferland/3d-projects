import { readFile, writeFile, mkdir } from "node:fs/promises";
import { createOpenSCAD } from "openscad-wasm-prebuilt";

const part = process.argv[2] ?? "A";
const compiler = await createOpenSCAD({ noInitialRun: true, print: console.log, printErr: console.error });
const instance = compiler.getInstance();
const source = (await readFile("independent-cutlery.scad", "utf8"))
  .replace('part = "A";', `part = "${part}";`);
instance.FS.writeFile("/model.scad", source);
instance.callMain(["/model.scad", "-o", "/output.stl"]);
await mkdir("independent-exports", { recursive: true });
await writeFile(`independent-exports/cutlery_${part}.stl`, instance.FS.readFile("/output.stl"));
