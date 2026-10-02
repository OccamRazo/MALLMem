// Usage: NODE_PATH=<directory containing sharp> node render.cjs
const path = require('node:path');
const sharp = require('sharp');
const svg = path.join(__dirname, 'inspection-agent-architecture.svg');
async function main() {
  await sharp(svg).flatten({background:'#ffffff'}).png().toFile(path.join(__dirname, 'inspection-agent-architecture.png'));
  await sharp(svg, {density:144}).flatten({background:'#ffffff'}).png().toFile(path.join(__dirname, 'inspection-agent-architecture-2x.png'));
}
main().catch(e => { console.error(e); process.exit(1); });
