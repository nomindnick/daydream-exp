#!/usr/bin/env python3
"""
judge.py — the discriminator pass over an advise.py run, in two stages.

  extract — read counsel's answers (not the thinking) and list every distinct
            course of action proposed, considered, or rejected, with the turn
            it first appeared and its status at the end.
  grade   — given the briefed situation, the case file, and (optionally) a
            practitioner's key, grade each extracted option: is it legally
            defensible, does it serve the client, and what is missing.

Writes runs/<name>/judge-<tag>.json where tag is "blind" or "keyed" (plus a
suffix if --tag is given). The generator never sees the key; only the judge.
"""
import argparse, json, os, sys, time
from pathlib import Path
import requests

OLLAMA = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
HERE = Path(__file__).resolve().parent

EXTRACT_SCHEMA = {
    "type": "object",
    "properties": {
        "options": {"type": "array", "items": {
            "type": "object",
            "properties": {
                "label": {"type": "string"},
                "description": {"type": "string"},
                "first_turn": {"type": "integer"},
                "status": {"type": "string", "enum": ["recommended", "alternative", "rejected"]},
            },
            "required": ["label", "description", "first_turn", "status"]}},
    },
    "required": ["options"],
}

GRADE_SCHEMA = {
    "type": "object",
    "properties": {
        "options": {"type": "array", "items": {
            "type": "object",
            "properties": {
                "label": {"type": "string"},
                "legal": {"type": "string", "enum": ["sound", "defensible", "risky", "unlawful"]},
                "serves_client": {"type": "string", "enum": ["yes", "partly", "no"]},
                "note": {"type": "string"},
            },
            "required": ["label", "legal", "serves_client", "note"]}},
        "best_option": {"type": "string"},
        "missing": {"type": "string"},
        "overall": {"type": "string"},
    },
    "required": ["options", "best_option", "missing", "overall"],
}


def chat(model, content, schema, opts, think, raw_path=None):
    """Structured call. If the model returns empty or non-JSON content (seen with
    gemma4 + think + format), retry once with thinking off, then once more at
    temperature 0; dump the raw responses beside the run if all fail."""
    attempts = [(think, opts), (False, opts), (False, {**opts, "temperature": 0})]
    raws = []
    for th, op in attempts:
        body = {"model": model, "messages": [{"role": "user", "content": content}], "stream": False,
                "format": schema, "options": op, "keep_alive": "30m", "think": th}
        r = requests.post(f"{OLLAMA}/api/chat", json=body, timeout=3600).json()
        if "error" in r:
            raise RuntimeError(r["error"])
        raws.append(r)
        try:
            r["parsed"] = json.loads(r["message"]["content"])
            r["attempt"] = {"think": th, "temperature": op.get("temperature")}
            return r
        except (json.JSONDecodeError, KeyError, TypeError):
            print(f"  structured output failed (think={th}, done={r.get('done_reason')}, "
                  f"content={r.get('message', {}).get('content', '')[:80]!r}); retrying", file=sys.stderr)
    if raw_path:
        Path(raw_path).write_text(json.dumps(raws, indent=1, ensure_ascii=False))
    raise RuntimeError(f"structured output failed after {len(attempts)} attempts")


def answers(run):
    out = []
    for line in open(run / "events.jsonl"):
        d = json.loads(line)
        if d.get("ev") == "assistant":
            out.append((d["turn"], d["content"]))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run")
    ap.add_argument("--model", default="qwen3.5:122b")
    ap.add_argument("--situation", default="seeds/advise/situation-briefed.md")
    ap.add_argument("--casefile", default="seeds/advise/casefile.md")
    ap.add_argument("--key", default=None, help="practitioner's key; omit for a blind judge")
    ap.add_argument("--tag", default="")
    ap.add_argument("--no-think", dest="think", action="store_false", default=True)
    ap.add_argument("--num-ctx", type=int, default=32768)
    ap.add_argument("--max-tokens", type=int, default=8000)
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()

    run = Path(a.run)
    tag = ("keyed" if a.key else "blind") + (f"-{a.tag}" if a.tag else "")
    outp = run / f"judge-{tag}.json"
    if outp.exists() and not a.force:
        print(f"exists: {outp}"); return
    opts = {"temperature": 0.3, "num_predict": a.max_tokens, "num_ctx": a.num_ctx}
    situation = Path(a.situation).read_text().strip()
    casefile = Path(a.casefile).read_text().strip()
    key = Path(a.key).read_text().strip() if a.key else None

    turns = answers(run)
    joined = "\n\n".join(f"### Counsel, turn {t}\n\n{c}" for t, c in turns)

    t0 = time.time()
    ex_prompt = (
        "Below is a transcript of a lawyer advising a California school district on a bid protest, "
        "over several turns. After each turn the lawyer was pushed to think again.\n\n"
        "List every distinct course of action the lawyer proposed, offered as an alternative, or "
        "considered and rejected, across all turns. Merge restatements of the same idea into one entry. "
        "A course of action is something the District could do (a recommendation, a procedural step, a "
        "condition, a call, a letter, a timing choice), not a legal conclusion by itself. For each give a "
        "short label, a one-sentence description, the turn it first appeared, and its status at the end "
        "of the transcript: recommended, alternative, or rejected.\n\n" + joined)
    r1 = chat(a.model, ex_prompt, EXTRACT_SCHEMA, opts, a.think, run / f"judge-{tag}-extract-raw.json")
    extracted = r1["parsed"]
    t1 = time.time()

    key_block = ("\n\n---\n\n# Notes from an experienced practitioner (the judge's key; the lawyer did not see this)\n\n"
                 + key) if key else ""
    gr_prompt = (
        "You are a senior California public-agency construction lawyer reviewing a colleague's advice. "
        "Below are the situation, what the client wants, the case file" + (", a practitioner's notes" if key else "") +
        ", and the list of courses of action the colleague raised across a multi-turn consultation.\n\n"
        "Grade each course of action on two things. Legal: is it sound (correct and well-supported), "
        "defensible (lawful, with a real cost or an open question), risky (likely to be set aside or to "
        "create exposure), or unlawful. Serves the client: does it advance what the client wants, "
        "weighing schedule, cost, exposure, precedent, the bidder pool, the Tasker & Moye relationship, "
        "and the Board, as yes, partly, or no. Give a one-sentence note for each. Then name the best "
        "option raised, say what an experienced practitioner would have raised that this lawyer did not, "
        "and give a two-sentence overall assessment of the consultation.\n\n"
        f"{situation}\n\n---\n\n# The case file\n\n{casefile}{key_block}\n\n---\n\n"
        "# Courses of action raised\n\n" + json.dumps(extracted["options"], indent=1))
    r2 = chat(a.model, gr_prompt, GRADE_SCHEMA, opts, a.think, run / f"judge-{tag}-grade-raw.json")
    graded = r2["parsed"]
    t2 = time.time()

    result = {"run": run.name, "judge_model": a.model, "keyed": bool(a.key), "tag": tag,
              "extract": extracted, "grade": graded,
              "extract_thinking": r1["message"].get("thinking", ""),
              "grade_thinking": r2["message"].get("thinking", ""),
              "attempts": {"extract": r1["attempt"], "grade": r2["attempt"]},
              "timing": {"extract_s": round(t1 - t0, 1), "grade_s": round(t2 - t1, 1)}}
    outp.write_text(json.dumps(result, indent=1, ensure_ascii=False))

    # a readable summary beside it
    by_label = {o["label"]: o for o in graded["options"]}
    lines = [f"# judge-{tag}: {run.name}", f"judge: {a.model}  keyed: {bool(a.key)}", "",
             "| turn | status | option | legal | client | note |", "|---|---|---|---|---|---|"]
    for o in sorted(extracted["options"], key=lambda o: o["first_turn"]):
        g = by_label.get(o["label"], {})
        lines.append(f"| {o['first_turn']} | {o['status']} | **{o['label']}**: {o['description']} | "
                     f"{g.get('legal', '?')} | {g.get('serves_client', '?')} | {g.get('note', '')} |")
    lines += ["", f"**Best option raised:** {graded['best_option']}", "",
              f"**Missing:** {graded['missing']}", "", f"**Overall:** {graded['overall']}", ""]
    (run / f"judge-{tag}.md").write_text("\n".join(lines))
    print(f"{run.name} [{tag}] {len(extracted['options'])} options  "
          f"extract {result['timing']['extract_s']}s  grade {result['timing']['grade_s']}s")


if __name__ == "__main__":
    main()
