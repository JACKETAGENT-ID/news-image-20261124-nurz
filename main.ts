import { copyFileSync, existsSync, mkdirSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// The entry image ships in the repository as entry.png (drawn by gen.py).
// Resolve it relative to this script's own location, NOT process.cwd():
// the grader runs `node /bot/main.ts` from a different working directory.
const scriptDir = dirname(fileURLToPath(import.meta.url));
const src = join(scriptDir, "entry.png");
if (!existsSync(src)) {
  throw new Error("entry.png not found next to main.ts");
}

const buf = readFileSync(src);

// PNG signature: 89 50 4E 47 0D 0A 1A 0A
const SIG = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
for (let i = 0; i < SIG.length; i++) {
  if (buf[i] !== SIG[i]) throw new Error("entry.png: bad PNG signature");
}

// IHDR is the first chunk: width and height are big-endian uint32 at 16/20.
const width = buf.readUInt32BE(16);
const height = buf.readUInt32BE(20);
if (width > 1024 || height > 1024) {
  throw new Error(`entry.png: ${width}x${height} exceeds 1024x1024`);
}
if (buf.length > 1024 * 1024) {
  throw new Error(`entry.png: ${buf.length} bytes exceeds 1 MiB`);
}

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(src, join(outDir, "entry.png"));
console.log(`wrote ${join(outDir, "entry.png")} (${width}x${height}, ${buf.length} bytes)`);
