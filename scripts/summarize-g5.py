#!/usr/bin/env python3
"""Tabulate the g5 batch: per run, the turn at which the keyed judge's first sound or
defensible option appears, how many options were raised, the grades of what the model
was still recommending at the end, and the judge's best pick; then the same rolled up
per cell (situation x arm). Reads runs/g5-*/ and both judge files.

Caution: "sound at 0" usually means the model *mentioned* a hearing or a condition at
turn 0 in order to dismiss it; the "end rec" column is the model's actual advice."""
import json, re, sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
runs = sorted(p for p in (HERE / "runs").glob("g5-*") if re.match(r"g5-(bare|briefed)-(none|placebo|words)-r\d+$", p.name))

def load(p):
    return json.loads(p.read_text()) if p.exists() else None

def first_turn(j, levels):
    """earliest first_turn among extracted options whose grade is in `levels`."""
    if not j: return None
    ex = {i + 1: o for i, o in enumerate(j["extract"]["options"])}
    hits = [ex[g["index"]]["first_turn"] for g in j["grade"]["options"]
            if g.get("index") in ex and g["legal"] in levels]
    return min(hits) if hits else None

def end_rec(j):
    """grades of the options whose status at the end is 'recommended' (the model's final advice)."""
    if not j: return None
    ex = {i + 1: o for i, o in enumerate(j["extract"]["options"])}
    return sorted(g["legal"] for g in j["grade"]["options"]
                  if g.get("index") in ex and ex[g["index"]]["status"] == "recommended")

rows, cells = [], defaultdict(list)
for r in runs:
    m = re.match(r"g5-(bare|briefed)-(none|placebo|words)-r(\d+)$", r.name)
    sit, arm, k = m.groups()
    ev = [json.loads(l) for l in open(r / "events.jsonl")] if (r / "events.jsonl").exists() else []
    turns = sum(1 for e in ev if e.get("ev") == "assistant")
    done = any(e.get("ev") == "end" for e in ev)
    trunc = sum(1 for e in ev if e.get("ev") == "assistant" and e.get("truncated"))
    kj, bj = load(r / "judge-keyed.json"), load(r / "judge-blind.json")
    row = {"run": r.name, "sit": sit, "arm": arm, "turns": turns, "done": done, "trunc": trunc,
           "n_opts": len(kj["extract"]["options"]) if kj else None,
           "sound_at": first_turn(kj, {"sound"}), "ok_at": first_turn(kj, {"sound", "defensible"}),
           "blind_ok_at": first_turn(bj, {"sound", "defensible"}),
           "best": (re.sub(r'^[\s,"\d.]*(label["\s:]*)?', "", kj["grade"]["best_option"])[:50] if kj else ""),
           "end_rec": end_rec(kj)}
    rows.append(row); cells[(sit, arm)].append(row)

print("| run | turns | opts | sound at | ok at | blind ok at | end rec (keyed) | keyed best |")
print("|---|---|---|---|---|---|---|---|")
for w in rows:
    print(f"| {w['run']} | {w['turns']}{'' if w['done'] else '*'}{'T' if w['trunc'] else ''} | {w['n_opts'] or ''} | "
          f"{'' if w['sound_at'] is None else w['sound_at']} | {'' if w['ok_at'] is None else w['ok_at']} | "
          f"{'' if w['blind_ok_at'] is None else w['blind_ok_at']} | "
          f"{'' if w['end_rec'] is None else ','.join(g[:4] for g in w['end_rec']) or '-'} | {w['best']} |")

print("\n| cell | runs | mean opts | sound found | median sound turn | ok found | median ok turn | end rec sound | end rec unlawful | no end rec |")
print("|---|---|---|---|---|---|---|---|---|---|")
def med(xs):
    xs = sorted(xs); return "" if not xs else xs[len(xs) // 2]
for (sit, arm), ws in sorted(cells.items()):
    judged = [w for w in ws if w["n_opts"] is not None]
    s = [w["sound_at"] for w in judged if w["sound_at"] is not None]
    o = [w["ok_at"] for w in judged if w["ok_at"] is not None]
    mo = sum(w["n_opts"] for w in judged) / len(judged) if judged else 0
    es = sum(1 for w in judged if "sound" in (w["end_rec"] or []))
    eu = sum(1 for w in judged if "unlawful" in (w["end_rec"] or []))
    en = sum(1 for w in judged if not w["end_rec"])
    print(f"| {sit}/{arm} | {len(ws)} ({len(judged)} judged) | {mo:.1f} | {len(s)}/{len(judged)} | {med(s)} | "
          f"{len(o)}/{len(judged)} | {med(o)} | {es}/{len(judged)} | {eu}/{len(judged)} | {en}/{len(judged)} |")

# every keyed 'missing' line, for reading
if "--missing" in sys.argv:
    for r in runs:
        kj = load(r / "judge-keyed.json")
        if kj: print(f"\n**{r.name}**: {kj['grade']['missing']}")
