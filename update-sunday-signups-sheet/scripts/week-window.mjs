#!/usr/bin/env node
// Print the CIW reporting window: Monday 12:00 PM Asia/Manila rollover.
// currentCutoff = most recent Monday 12:00 that has passed; window = [cutoff-7d, cutoff).
// Optional --now "2026-06-22T10:00:00+08:00" to override (Date.now is fine in plain Node).

const args = new Map();
for (let i = 2; i < process.argv.length; i += 1) {
  if (process.argv[i].startsWith("--")) { args.set(process.argv[i].slice(2), process.argv[i + 1]); i += 1; }
}

const PH = 8 * 60; // minutes
const now = args.has("now") ? new Date(args.get("now")) : new Date();
// Shift to PH wall clock
const phNow = new Date(now.getTime() + (PH * 60 * 1000) + now.getTimezoneOffset() * 60 * 1000);
// Find most recent Monday 12:00 PH that has passed
const cutoff = new Date(phNow);
const day = cutoff.getDay(); // 0 Sun .. 1 Mon
const daysSinceMon = (day + 6) % 7;
cutoff.setDate(cutoff.getDate() - daysSinceMon);
cutoff.setHours(12, 0, 0, 0);
if (cutoff > phNow) cutoff.setDate(cutoff.getDate() - 7);
const start = new Date(cutoff); start.setDate(start.getDate() - 7);

const iso = (d) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}T${String(d.getHours()).padStart(2, "0")}:${String(d.getMinutes()).padStart(2, "0")}:00`;
console.log(JSON.stringify({ tz: "Asia/Manila", startISO: iso(start), endISO: iso(cutoff), note: "[start, end) Monday-noon window" }, null, 2));
