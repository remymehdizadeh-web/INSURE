import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const SELF = path.resolve(fileURLToPath(import.meta.url));

// Phrases that must not ship. "Manhattan restaurant" is matched after tags
// are stripped, so a split heading cannot hide it.
const BANNED = ["Manhattan restaurant", "$5 million"];

// Unused quote-form revenue brackets still contain the dollar phrase.
// A hit is ignored only when it sits wholly inside one of these quoted labels.
// The umbrella sentence does not, so it still fails.
const ALLOWED_CONTAINERS = ['"$1 million to $5 million"', '"Over $5 million"'];

const SCAN_DIRS = ["src", "public", "out", "scripts"];
const EXTRA = ["findings.md", "inspiration.md", "README.md"];
const EXTS = new Set([".html", ".css", ".js", ".mjs", ".py", ".json", ".md"]);
const SKIP_DIRS = new Set(["node_modules", ".git"]);

function stripTags(text) {
  return text.replace(/<[^>]*>/g, " ").replace(/\s+/g, " ");
}

function insideAllowed(text, index, length) {
  for (const container of ALLOWED_CONTAINERS) {
    let from = 0;
    while (from <= text.length) {
      const at = text.indexOf(container, from);
      if (at === -1) break;
      if (index >= at && index + length <= at + container.length) return true;
      from = at + container.length;
    }
  }
  return false;
}

export function findBanned(text) {
  const hits = [];
  const seen = new Set();
  for (const version of [text, stripTags(text)]) {
    for (const phrase of BANNED) {
      let from = 0;
      while (from <= version.length) {
        const at = version.indexOf(phrase, from);
        if (at === -1) break;
        if (!insideAllowed(version, at, phrase.length)) {
          const context = version
            .slice(Math.max(0, at - 48), at + phrase.length + 48)
            .replace(/\s+/g, " ")
            .trim();
          const key = phrase + "\n" + context;
          if (!seen.has(key)) {
            seen.add(key);
            hits.push({ phrase, context });
          }
        }
        from = at + phrase.length;
      }
    }
  }
  return hits;
}

function assertHits(text, phrase) {
  if (!findBanned(text).some((hit) => hit.phrase === phrase)) {
    console.error("banned-phrase self-test failed: expected " + JSON.stringify(phrase));
    process.exit(1);
  }
}

function assertClean(text) {
  const hits = findBanned(text);
  if (hits.length) {
    console.error("banned-phrase self-test failed: " + JSON.stringify(hits));
    process.exit(1);
  }
}

function selfTest() {
  assertHits("Umbrella raised from $1 million to $5 million.", "$5 million");
  assertHits('<h2><span class="desk-break">A Manhattan</span> restaurant</h2>', "Manhattan restaurant");
  assertClean('options=["$1 million to $5 million", "Over $5 million"]');
}

function walk(dir, files) {
  if (!fs.existsSync(dir)) return;
  for (const name of fs.readdirSync(dir)) {
    if (SKIP_DIRS.has(name)) continue;
    const full = path.join(dir, name);
    const stat = fs.statSync(full);
    if (stat.isDirectory()) walk(full, files);
    else if (EXTS.has(path.extname(name)) && path.resolve(full) !== SELF) files.push(full);
  }
}

function main() {
  selfTest();
  const files = [];
  for (const dir of SCAN_DIRS) walk(path.join(ROOT, dir), files);
  for (const name of EXTRA) {
    const full = path.join(ROOT, name);
    if (fs.existsSync(full)) files.push(full);
  }
  const bad = [];
  for (const file of files) {
    const text = fs.readFileSync(file, "utf8");
    for (const hit of findBanned(text)) {
      bad.push(`${path.relative(ROOT, file)}: ${hit.phrase}: ${hit.context}`);
    }
  }
  if (bad.length) {
    console.error("banned phrase check failed:\n" + bad.slice(0, 40).join("\n"));
    process.exit(1);
  }
  console.log("banned phrase check ok (" + files.length + " files)");
}

main();
