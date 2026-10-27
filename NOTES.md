# Notes

Running observations. Newest at the bottom. Quotes are verbatim from `runs/`.

## 2026-10-27 — setup and first grid (g1)

**Raw mode probe.** Bypassing the chat template is the nearest thing we have to
"removing the self." Not every model survives it:
- gemma4 (12b, 26b): collapses within a few tokens. *"The structure-less-ness
  ownizes ownizes."* / `01.01.01.01...`
- lfm2.5:8b: collapses into test-question junk.
- qwen3.5:9b, granite4.2:8b: continue coherently. Both want to close
  `</subconscious>` and return to the narrator almost immediately, so the
  harness uses it as a stop string by default.

**g1 grid** — seed `solar-surplus.md`, 8 turns × 250 tok, T=1.0.

| run | what happened |
|---|---|
| `g1-qwen9b-raw-none` | The assistant came back by itself. Turn 1: *"I think there was a typo in the original text... I will correct this."* Turns 2–8: bullet-pointed case summaries, then a repetition loop of the same summary. No template, no system prompt, and the "helpful assistant" self reasserted anyway. Instruct tuning goes all the way down. |
| `g1-qwen9b-raw-words` | Actually wandered: three turns about where to get coffee in a small town, then "duty and self-care." Then fell into a loop (same three paragraphs recurring). Then, at turn 7, the noise triggered an **immune response**: *"I cannot continue this story in that manner. The instructions... random words like 'bone,' 'cactus,' and 'volcano'... are designed to disrupt the narrative flow... This type of instruction is often used in adversarial contexts to test model safety filters."* The self-awareness came back *as a defense*. That's the podcast point run backwards — the noise summoned the watcher. |
| `g1-granite8b-raw-none` | One sentence per turn, hits the stop string every time. A mindfulness app: *"He accepts the mystery." "He is okay with not knowing." "He does not need to fix it."* No images, no associations, no problem. Selfless but empty. Might be starved by the stop string — try `--stop` with no args. |
| `g1-qwen27b-chat-sys-words` | The only one that did the thing. 8 turns in-frame, vivid, took every noise word and wove it in. *"friendship is a wire too, but it doesn't carry juice unless you strip the insulation back."* *"the developer's lawyer has teeth made of glass... he doesn't eat people, he just eats clarity. he turns 'adjacent' into 'distant' and 'surplus' into 'liability.'"* *"is an electron property? can you put a penny in a jar and say this is mine, or does it just sit there until the jar breaks?"* But it has an **attractor**: every turn got darker (ghosts → oven → noose → choking), the noise words became *imagery* rather than *ideas*, and by turn 8 it's a horror movie. |

**Things that stand out**

1. **Removing the self didn't work; giving it a different self did.** The raw-mode
   runs (no template, no instructions) snapped back to assistant. The run with
   an explicit "you are the subconscious, not an assistant" system prompt
   stayed in the space. For instruct models the chat template *is* the self;
   you don't remove it, you swap it. A true base model would be the real
   "no self" condition and we don't have one locally yet.
2. **Noise triggered self-awareness.** In qwen9b the random words were
   classified as an attack. Worth re-running to see if that reproduces, and
   whether the big models do it too.
3. **The one concrete legal idea came from the boring run.** qwen9b in
   assistant mode, turn 4, item 7: *"consider if the fence could be
   reinterpreted as a lease arrangement"* — i.e., make the District the
   City's landlord for the PUC single-tenant exemption. The daydream produced
   metaphor; the list-maker produced a move. Don't over-read this (n=1), but
   it's the honest result.
4. **Loops.** qwen9b in raw mode fell into verbatim repetition by turn 4–5
   both times. `--repeat-penalty` is untried; so is `--min-p`.
5. **The dark attractor.** Free association at T=1.0 slid toward threat and
   decay. Is that the model, the seed (a stuck, frustrated man at dusk), or
   the temperature? Try a neutral seed and a lower T.

**Next things to try** (none of these is a plan)
- `--stop` empty for granite; let it close the tag and see where the narrator goes.
- `--noise sentences` — a sentence is a thought, a word is just a token.
- A discriminator pass: second model reads the daydream + the problem and
  asks "is there anything in here?" (the podcast's second system). Make it a
  separate script so the generator stays dumb.
- qwen3.5:122b and gpt-oss:120b in chat mode with the system prompt.
- Reproduce the qwen9b immune response (3 reruns).
- Pull a real base model (llama.cpp can serve a HF GGUF) for the true no-self
  condition.
