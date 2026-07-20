#!/usr/bin/env node
// Write a single row of values to the CIW / SIGNUPS tab via Sheets API + ADC.
// Usage: node sheets-write-range.mjs --range "'CIW / SIGNUPS'!E179:H179" --values "19,10,21,37"

import { execFileSync } from "node:child_process";

const SPREADSHEET_ID = "1bUdcidjNrdxC4fyqgqIxWfQ3N6YvFDXY2gpQFts_Vzs";
const args = new Map();
for (let i = 2; i < process.argv.length; i += 1) {
  if (process.argv[i].startsWith("--")) { args.set(process.argv[i].slice(2), process.argv[i + 1]); i += 1; }
}
const range = args.get("range");
if (!range || !args.has("values")) { console.error('Usage: --range "\'CIW / SIGNUPS\'!E179:H179" --values "19,10,21,37"'); process.exit(1); }
const values = [args.get("values").split(",").map((v) => (v.trim() === "" ? "" : isNaN(Number(v)) ? v.trim() : Number(v)))];

const quotaProject = args.get("quota-project") || process.env.GOOGLE_CLOUD_QUOTA_PROJECT || "gen-lang-client-0705704834";
const token = execFileSync("gcloud", ["auth", "application-default", "print-access-token"], { encoding: "utf8" }).trim();
const url = `https://sheets.googleapis.com/v4/spreadsheets/${SPREADSHEET_ID}/values/${encodeURIComponent(range)}?valueInputOption=USER_ENTERED`;

const res = await fetch(url, {
  method: "PUT",
  headers: { Authorization: `Bearer ${token}`, "x-goog-user-project": quotaProject, "Content-Type": "application/json" },
  body: JSON.stringify({ range, majorDimension: "ROWS", values })
});
const body = await res.text();
if (!res.ok) throw new Error(`Sheets write failed ${res.status}: ${body}`);
console.log(body);
