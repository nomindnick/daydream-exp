# daydream-exp

An open-ended experiment: put a local LLM in a "subconscious" space and let it
free-associate around a legal problem, with and without random noise injected
into the stream. No hypothesis, no eval. Walk into the chaos; see if anything
clarifies.

## Where this came from

A neuroscientist on creativity, paraphrased:

1. The generative part of creativity — letting the mind wander and combine
   unrelated things — is subconscious. A *different* system later discriminates
   good ideas from bad.
2. To get into a creative flow state (like a musical improviser) you have to
   lose self-awareness. The self gets out of the way.

Plus Tim Kellogg's observations on stateful agents: a model without a strong
identity spirals ("model collapse"). Maybe the thing we want is adjacent to
that spiral, not opposite it.

The bigger question this sits inside: what does legal judgment and creativity
look like when the baseline legal knowledge and reasoning are on-demand?

## Two starting ideas

- **Literal daydreaming.** A narrative of an attorney working a hard problem,
  who then lets it go. Then `<subconscious>` and the model just continues.
  Each turn is `<subconscious continues>`.
- **Noise injection.** True-random words (or one-sentence expansions of them)
  dropped into the stream as `<subconscious noise>` to light up unrelated
  regions of the latent space and see what the model does with them.

## Running

```
python3 daydream.py --help
python3 daydream.py --model qwen3.5:9b --mode raw --noise none
python3 daydream.py --model qwen3.5:9b --mode raw --noise words --noise-every 2 --noise-n 5
python3 daydream.py --model qwen3.5:27b --mode chat --system seeds/system-subconscious.md --noise sentences
```

Every run writes `runs/<name>/`:
- `config.json` — every knob
- `events.jsonl` — seed, each noise draw, each turn (text, tokens, t/s, context used)
- `transcript.md` — the readable version
- `document.txt` — raw mode only: the single growing text the model saw

Knobs worth playing with: `--mode raw|chat`, `--temperature`, `--min-p`,
`--stop` (default stops the model from closing `</subconscious>` and
returning to narrator; pass `--stop` alone to let it), `--noise-source dict`
(the whole 235k-word system dictionary — mostly obscure), `--noise-model`.

Models here are all instruct-tuned. Raw mode strips the chat template, which
is the closest thing we have to removing the model's "self." Only some models
survive that (see NOTES.md).

## Layout

- `daydream.py` — the harness, one file, meant to be hacked on
- `seeds/` — narrative seeds and system prompts
- `words/` — word lists for noise
- `runs/` — every run, committed, so the chaos is kept
- `NOTES.md` — running observations
