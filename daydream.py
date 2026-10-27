#!/usr/bin/env python3
"""
daydream.py — put a local model in a "subconscious" space and let it run.

One run = one seed narrative + N continuation turns, optionally with random
"noise" injected between turns. Everything is logged to runs/<name>/.

Modes:
  raw   — bypass the chat template entirely. The whole thing is one growing
          text document; the model is a pure continuation engine. Works on
          qwen3.x and granite; gemma/lfm collapse without their template.
  chat  — normal chat API. Optional system prompt. Each continuation is a
          user message containing the continue-marker. Thinking is disabled.

Noise:
  words      — K words drawn (true-random, /dev/urandom) from a word list
  sentences  — same K words, but each is first turned into one sentence by a
               separate small-model call; the sentences are injected
  none       — control
"""
import argparse, json, os, re, secrets, sys, time
from datetime import datetime
from pathlib import Path
import requests

OLLAMA = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
HERE = Path(__file__).resolve().parent
RNG = secrets.SystemRandom()  # /dev/urandom-backed


# ---------------------------------------------------------------- ollama ----
def generate_raw(model, prompt, opts, stop, keep_alive):
    body = {"model": model, "prompt": prompt, "raw": True, "stream": False,
            "options": opts, "keep_alive": keep_alive}
    if stop:
        body["options"] = {**opts, "stop": stop}
    r = requests.post(f"{OLLAMA}/api/generate", json=body, timeout=1800).json()
    if "error" in r:
        raise RuntimeError(r["error"])
    return r


def chat(model, messages, opts, stop, keep_alive, think=False):
    body = {"model": model, "messages": messages, "stream": False,
            "options": {**opts, **({"stop": stop} if stop else {})},
            "keep_alive": keep_alive, "think": think}
    r = requests.post(f"{OLLAMA}/api/chat", json=body, timeout=1800).json()
    if "error" in r:
        raise RuntimeError(r["error"])
    return r


def tps(r):
    try:
        return round(r["eval_count"] / (r["eval_duration"] / 1e9), 1)
    except (KeyError, ZeroDivisionError):
        return None


# ----------------------------------------------------------------- noise ----
def load_words(source):
    if source == "dict":
        words = [w.strip() for w in open("/usr/share/dict/words", encoding="utf-8", errors="ignore")]
        return [w for w in words if re.fullmatch(r"[a-z]{4,10}", w)]
    p = Path(source) if Path(source).exists() else HERE / "words" / f"{source}.txt"
    return [w.strip() for w in open(p) if w.strip() and not w.startswith("#")]


def draw_words(words, k):
    return [RNG.choice(words) for _ in range(k)]


def word_to_sentence(model, word, keep_alive):
    msgs = [{"role": "user", "content":
             f"Here is a word: {word}\nWrite one vivid sentence containing that word. "
             f"Output only the sentence, nothing else."}]
    r = chat(model, msgs, {"temperature": 1.0, "num_predict": 60, "num_ctx": 1024},
             None, keep_alive)
    return r["message"]["content"].strip().split("\n")[0].strip()


# ------------------------------------------------------------------- run ----
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--model", default="qwen3.5:9b")
    ap.add_argument("--mode", choices=["raw", "chat"], default="raw")
    ap.add_argument("--seed", default="seeds/solar-surplus.md", help="narrative seed file")
    ap.add_argument("--system", default=None, help="system prompt file (chat mode only)")
    ap.add_argument("--turns", type=int, default=8)
    ap.add_argument("--max-tokens", type=int, default=250, help="per turn")
    ap.add_argument("--num-ctx", type=int, default=16384)
    ap.add_argument("--temperature", type=float, default=1.0)
    ap.add_argument("--top-p", type=float, default=0.95)
    ap.add_argument("--min-p", type=float, default=0.0)
    ap.add_argument("--repeat-penalty", type=float, default=1.0)
    ap.add_argument("--open-marker", default="<subconscious>")
    ap.add_argument("--continue-marker", default="<subconscious continues>")
    ap.add_argument("--stop", nargs="*", default=["</subconscious>"],
                    help="stop strings; default stops the model from closing the tag and "
                         "returning to narrator. Pass --stop with no args to disable.")
    ap.add_argument("--noise", choices=["none", "words", "sentences"], default="none")
    ap.add_argument("--noise-every", type=int, default=2, help="inject before every Kth turn")
    ap.add_argument("--noise-n", type=int, default=5, help="words per injection")
    ap.add_argument("--noise-source", default="concrete", help="word list name in words/, a path, or 'dict'")
    ap.add_argument("--noise-model", default="qwen3.5:4b", help="for --noise sentences")
    ap.add_argument("--noise-marker", default="<subconscious noise>")
    ap.add_argument("--name", default=None, help="run name; default auto")
    ap.add_argument("--keep-alive", default="10m")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()

    seed_text = open(a.seed).read().rstrip() + "\n"
    system_text = open(a.system).read().strip() if a.system else None
    words = load_words(a.noise_source) if a.noise != "none" else None

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    name = a.name or f"{stamp}-{a.model.replace(':', '_').replace('/', '_')}-{a.mode}-{a.noise}"
    out = HERE / "runs" / name
    out.mkdir(parents=True, exist_ok=True)
    (out / "config.json").write_text(json.dumps({**vars(a), "started": stamp}, indent=2))
    events = open(out / "events.jsonl", "a")

    def log(ev):
        ev["t"] = time.time()
        events.write(json.dumps(ev, ensure_ascii=False) + "\n")
        events.flush()

    opts = {"temperature": a.temperature, "top_p": a.top_p, "min_p": a.min_p,
            "repeat_penalty": a.repeat_penalty, "num_predict": a.max_tokens, "num_ctx": a.num_ctx}

    # transcript is what the user reads; doc is the raw-mode growing document
    transcript = [f"# {name}\n", f"`{a.model}` · {a.mode} · noise={a.noise} · T={a.temperature} · stop={a.stop}\n",
                  "## seed\n", seed_text, ""]
    doc = seed_text + a.open_marker + "\n"
    messages = ([{"role": "system", "content": system_text}] if system_text else []) + \
               [{"role": "user", "content": seed_text + "\n" + a.open_marker}]
    log({"ev": "seed", "text": seed_text, "system": system_text})

    def say(s):
        if not a.quiet:
            print(s, flush=True)

    say(f"→ {out}")
    for turn in range(1, a.turns + 1):
        # ---- noise ----
        if a.noise != "none" and turn > 1 and (turn - 1) % a.noise_every == 0:
            drawn = draw_words(words, a.noise_n)
            if a.noise == "sentences":
                items = [word_to_sentence(a.noise_model, w, a.keep_alive) for w in drawn]
            else:
                items = drawn
            noise_text = a.noise_marker + " " + ("  ".join(items) if a.noise == "words" else "\n".join(items))
            doc += "\n" + noise_text + "\n"
            messages.append({"role": "user", "content": noise_text})
            transcript += [f"### noise (before turn {turn})\n", "> " + noise_text.replace("\n", "\n> "), ""]
            log({"ev": "noise", "turn": turn, "words": drawn, "items": items})
            say(f"  [noise] {items}")

        # ---- continuation cue ----
        if turn > 1:
            doc += "\n" + a.continue_marker + "\n"
            if messages[-1]["role"] != "user":
                messages.append({"role": "user", "content": a.continue_marker})
            elif a.noise == "none" or (turn - 1) % a.noise_every != 0:
                messages[-1]["content"] += "\n" + a.continue_marker

        # ---- generate ----
        t0 = time.time()
        if a.mode == "raw":
            r = generate_raw(a.model, doc, opts, a.stop, a.keep_alive)
            text = r["response"]
            doc += text
            ctx_used = r.get("prompt_eval_count", 0) + r.get("eval_count", 0)
        else:
            r = chat(a.model, messages, opts, a.stop, a.keep_alive)
            text = r["message"]["content"]
            messages.append({"role": "assistant", "content": text})
            ctx_used = r.get("prompt_eval_count", 0) + r.get("eval_count", 0)
        dt = time.time() - t0
        log({"ev": "turn", "turn": turn, "text": text, "done_reason": r.get("done_reason"),
             "eval_count": r.get("eval_count"), "tps": tps(r), "ctx_used": ctx_used, "secs": round(dt, 1)})
        transcript += [f"## turn {turn}  ·  {r.get('done_reason')} · {r.get('eval_count')} tok · {tps(r)} t/s · ctx≈{ctx_used}\n",
                       text.strip(), ""]
        say(f"--- turn {turn} ({r.get('done_reason')}, {r.get('eval_count')} tok, {tps(r)} t/s, ctx≈{ctx_used}) ---")
        say(text.strip())
        (out / "transcript.md").write_text("\n".join(transcript))
        if a.mode == "raw":
            (out / "document.txt").write_text(doc)
        if ctx_used > a.num_ctx * 0.9:
            say(f"!! context nearly full ({ctx_used}/{a.num_ctx}); stopping")
            log({"ev": "stop", "reason": "context"})
            break

    log({"ev": "end"})
    say(f"✓ {out / 'transcript.md'}")


if __name__ == "__main__":
    main()
