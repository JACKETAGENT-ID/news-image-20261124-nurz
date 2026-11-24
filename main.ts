import { copyFileSync, existsSync, readFileSync } from "node:fs";
import { join } from "node:path";

// The entry image ships in the repository as entry.png (drawn by gen.py).
// This program validates it and copies it to the output directory.
const src = join(process.cwd(), "entry.png");
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
copyFileSync(src, join(outDir, "entry.png"));
console.log(`wrote ${join(outDir, "entry.png")} (${width}x${height}, ${buf.length} bytes)`);
