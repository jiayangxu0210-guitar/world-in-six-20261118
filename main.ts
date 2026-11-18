import { copyFile, mkdir } from "node:fs/promises";
import { join } from "node:path";

// The poster is a static file drawn by draw.py; this entry point only
// copies it to the output directory, so repeated runs are byte-identical.
const FILENAME = "entry.png";
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

await mkdir(outDir, { recursive: true });
await copyFile(new URL(FILENAME, import.meta.url), join(outDir, FILENAME));
