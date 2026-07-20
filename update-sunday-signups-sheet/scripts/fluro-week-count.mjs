#!/usr/bin/env node
// Count Fluro interaction submissions in the Monday-noon PH window.
// Usage: node fluro-week-count.mjs --definition mnlSignUpForAConnectGroup [--start 2026-06-15T12:00:00] [--end 2026-06-22T12:00:00]

import fs from "node:fs";
import os from "node:os";

const args = new Map();
for (let i = 2; i < process.argv.length; i += 1) {
  if (process.argv[i].startsWith("--")) { args.set(process.argv[i].slice(2), process.argv[i + 1]); i += 1; }
}
if (!args.has("definition")) { console.error("--definition required (e.g. mnlSignUpForAConnectGroup, signUpToServe)"); process.exit(1); }

function loadEnv(path) {
  if (!fs.existsSync(path)) return;
  for (const line of fs.readFileSync(path, "utf8").split(/\r?\n/)) {
    const t = line.trim();
    if (!t || t.startsWith("#")) continue;
    const i = t.indexOf("="); if (i < 0) continue;
    const k = t.slice(0, i).trim().replace(/^export\s+/, "");
    let v = t.slice(i + 1).trim();
    if ((v.startsWith('"') && v.endsWith('"')) || (v.startsWith("'") && v.endsWith("'"))) v = v.slice(1, -1);
    if (!process.env[k]) process.env[k] = v;
  }
}
loadEnv(`${os.homedir()}/.env`);
const token = process.env.FLURO_TOKEN || process.env.FLURO_SERVICE_TOKEN || process.env.FLURO_ADMIN_TOKEN;
if (!token) throw new Error("Missing FLURO_TOKEN");

const PH = "+08:00";
// Default window = the live Monday-noon Asia/Manila window (same logic as week-window.mjs),
// NOT a hardcoded date — otherwise you silently get the wrong week. Override with --start/--end.
function defaultWindowISO() {
  const PH_MIN = 8 * 60;
  const now = new Date();
  const phNow = new Date(now.getTime() + PH_MIN * 60 * 1000 + now.getTimezoneOffset() * 60 * 1000);
  const cutoff = new Date(phNow);
  const daysSinceMon = (cutoff.getDay() + 6) % 7;
  cutoff.setDate(cutoff.getDate() - daysSinceMon);
  cutoff.setHours(12, 0, 0, 0);
  if (cutoff > phNow) cutoff.setDate(cutoff.getDate() - 7);
  const s = new Date(cutoff); s.setDate(s.getDate() - 7);
  const iso = (d) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}T${String(d.getHours()).padStart(2, "0")}:${String(d.getMinutes()).padStart(2, "0")}:00`;
  return { startISO: iso(s), endISO: iso(cutoff) };
}
const win = defaultWindowISO();
const start = new Date(`${args.get("start") || win.startISO}${PH}`);
const end = new Date(`${args.get("end") || win.endISO}${PH}`);

const res = await fetch("https://api.fluro.io/content/_query?limit=5000&simple=false", {
  method: "POST",
  headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
  body: JSON.stringify({ _type: "interaction", definition: args.get("definition"), status: { $in: ["active", "draft", "archived"] } })
});
const text = await res.text();
if (!res.ok) throw new Error(`Fluro ${res.status}: ${text}`);
const rows = JSON.parse(text);
const inWin = rows.filter((r) => r.created && new Date(r.created) >= start && new Date(r.created) < end);
console.log(JSON.stringify({ definition: args.get("definition"), start: start.toISOString(), end: end.toISOString(), total: rows.length, windowCount: inWin.length }, null, 2));
