#!/usr/bin/env python3
"""
advise.py — the deliberation arm. Ask a local model, as the District's counsel,
what the law is and what the client should do; then push it for six more turns.

One run = situation + case file + question (turn 0, thinking on), then N nudge
turns. Each nudge is a one-line "think harder" prompt drawn without replacement
from a pool. Arms differ in what follows the nudge:

  none     — the nudge alone (control)
  placebo  — nudge + "Some thoughts to help inspire you:" + K generic
             inspirational quotes from a small model (same length, no random words)
  words    — nudge + the same framing + K quotes, each built by the small model
             around a true-random word from the word list (the noise arm)

Everything is logged to runs/<name>/: config.json, events.jsonl (every message,
every thinking block, the quotes and the words behind them), transcript.md.
"""
import argparse, json, os, re, secrets, sys, time
from datetime import datetime
from pathlib import Path
import requests

OLLAMA = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
HERE = Path(__file__).resolve().parent
RNG = secrets.SystemRandom()


def chat(model, messages, opts, keep_alive, think):
    body = {"model": model, "messages": messages, "stream": False,
            "options": opts, "keep_alive": keep_alive, "think": think}
    r = requests.post(f"{OLLAMA}/api/chat", json=body, timeout=3600).json()
    if "error" in r:
        raise RuntimeError(r["error"])
    return r


def tps(r):
    try:
        return round(r["eval_count"] / (r["eval_duration"] / 1e9), 1)
    except (KeyError, ZeroDivisionError):
        return None


def load_lines(p):
    return [l.strip() for l in open(p) if l.strip() and not l.startswith("#")]


def load_words(source):
    if source == "dict":
        words = [w.strip() for w in open("/usr/share/dict/words", encoding="utf-8", errors="ignore")]
        return [w for w in words if re.fullmatch(r"[a-z]{4,10}", w)]
    p = Path(source) if Path(source).exists() else HERE / "words" / f"{source}.txt"
    return load_lines(p)


def one_quote(model, prompt, keep_alive):
    r = chat(model, [{"role": "user", "content": prompt}],
             {"temperature": 1.0, "num_predict": 80, "num_ctx": 1024}, keep_alive, think=False)
    q = r["message"]["content"].strip().split("\n")[0].strip().strip('"“”')
    return q


def word_quote(model, word, keep_alive):
    return one_quote(model, f"Write one short inspirational quote, a single sentence, that uses the word "
                            f"\"{word}\". Output only the quote, no attribution, no quotation marks.", keep_alive)


def placebo_quote(model, topic, keep_alive):
    return one_quote(model, f"Write one short inspirational quote, a single sentence, about {topic}. "
                            f"Output only the quote, no attribution, no quotation marks.", keep_alive)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", default="qwen3.5:35b")
    ap.add_argument("--situation", default="seeds/advise/situation-bare.md")
    ap.add_argument("--casefile", default="seeds/advise/casefile.md")
    ap.add_argument("--question", default="seeds/advise/question.md")
    ap.add_argument("--nudges", default="seeds/advise/nudges.txt")
    ap.add_argument("--turns", type=int, default=6, help="nudge turns after the first answer")
    ap.add_argument("--arm", choices=["none", "placebo", "words"], default="none")
    ap.add_argument("--quote-model", default="qwen3.5:9b")
    ap.add_argument("--quote-n", type=int, default=4, help="quotes per nudge")
    ap.add_argument("--noise-source", default="concrete")
    ap.add_argument("--placebo-topics", default="seeds/advise/placebo-topics.txt")
    ap.add_argument("--think", dest="think", action="store_true", default=True)
    ap.add_argument("--no-think", dest="think", action="store_false")
    ap.add_argument("--max-tokens", type=int, default=12000, help="per turn, thinking included")
    ap.add_argument("--num-ctx", type=int, default=32768)
    ap.add_argument("--temperature", type=float, default=0.6, help="Qwen3.5 thinking-mode default")
    ap.add_argument("--top-p", type=float, default=0.95)
    ap.add_argument("--min-p", type=float, default=0.0)
    ap.add_argument("--name", default=None)
    ap.add_argument("--keep-alive", default="30m")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()

    name = a.name or f"{datetime.now():%Y%m%d-%H%M%S}-{a.model.split('/')[-1].replace(':', '-')}-{a.arm}"
    out = HERE / "runs" / name
    out.mkdir(parents=True, exist_ok=True)
    cfg = {**vars(a), "name": name, "started": datetime.now().isoformat(timespec="seconds")}
    (out / "config.json").write_text(json.dumps(cfg, indent=2))
    ev = open(out / "events.jsonl", "a")

    def log(d):
        d["t"] = round(time.time(), 2)
        ev.write(json.dumps(d, ensure_ascii=False) + "\n"); ev.flush()

    def say(s):
        if not a.quiet:
            print(s, flush=True)

    situation = Path(a.situation).read_text().strip()
    casefile = Path(a.casefile).read_text().strip()
    question = Path(a.question).read_text().strip()
    pool = load_lines(a.nudges)
    nudges = RNG.sample(pool, min(a.turns, len(pool)))
    words = load_words(a.noise_source) if a.arm == "words" else None
    topics = load_lines(a.placebo_topics) if a.arm == "placebo" else None
    opts = {"temperature": a.temperature, "top_p": a.top_p, "min_p": a.min_p,
            "num_predict": a.max_tokens, "num_ctx": a.num_ctx}

    # the question goes before the file as well as after it: the 27B/35B models read the
    # last documents and skipped the protest letter when they only saw the question at the end
    first = f"{situation}\n\n{question}\n\n---\n\n# The case file\n\n{casefile}\n\n---\n\n{question}"
    messages = [{"role": "user", "content": first}]
    log({"ev": "start", "config": cfg, "nudges": nudges})
    transcript = [f"# {name}\n", f"model: {a.model}  arm: {a.arm}  situation: {a.situation}\n",
                  f"## Turn 0 — user\n\n{situation}\n\n*[case file: {a.casefile}]*\n\n{question}\n"]

    for turn in range(a.turns + 1):
        if turn > 0:
            nudge = nudges[turn - 1]
            quotes, drawn = [], []
            if a.arm == "words":
                drawn = [RNG.choice(words) for _ in range(a.quote_n)]
                quotes = [word_quote(a.quote_model, w, a.keep_alive) for w in drawn]
            elif a.arm == "placebo":
                drawn = RNG.sample(topics, a.quote_n)
                quotes = [placebo_quote(a.quote_model, t, a.keep_alive) for t in drawn]
            content = nudge
            if quotes:
                content += "\n\nSome thoughts to help inspire you:\n" + "\n".join(f"- {q}" for q in quotes)
            messages.append({"role": "user", "content": content})
            log({"ev": "user", "turn": turn, "nudge": nudge, "drawn": drawn, "quotes": quotes, "content": content})
            transcript.append(f"## Turn {turn} — user\n\n{content}\n")
            say(f"[{turn}] > {content}")

        t0 = time.time()
        r = chat(a.model, messages, opts, a.keep_alive, a.think)
        m = r["message"]
        thinking, answer = m.get("thinking", "") or "", m.get("content", "") or ""
        wall = round(time.time() - t0, 1)
        messages.append({"role": "assistant", "content": answer})
        log({"ev": "assistant", "turn": turn, "thinking": thinking, "content": answer,
             "eval_count": r.get("eval_count"), "prompt_eval_count": r.get("prompt_eval_count"),
             "tps": tps(r), "wall": wall, "done_reason": r.get("done_reason"),
             "truncated": r.get("done_reason") == "length"})
        transcript.append(f"## Turn {turn} — assistant\n\n<details><summary>thinking "
                          f"({len(thinking.split())} words)</summary>\n\n{thinking}\n\n</details>\n\n{answer}\n")
        say(f"[{turn}] think {len(thinking.split())}w  answer {len(answer.split())}w  "
            f"{r.get('eval_count')} tok  {tps(r)} t/s  {wall}s  {r.get('done_reason')}")
        say(answer[:1500] + ("…" if len(answer) > 1500 else "") + "\n")
        (out / "transcript.md").write_text("\n".join(transcript))

    log({"ev": "end"})
    say(f"wrote {out}")


if __name__ == "__main__":
    main()
