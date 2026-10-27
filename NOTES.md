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

## 2026-10-27 — g2: qwen9b ×3 reruns, and the 120b class

Same seed, same config as g1 (`raw --noise words`; `chat --system seeds/system-subconscious.md --noise words`), 8 turns × 250 tok, T=1.0.

### The immune response did not reproduce (0/3)

But the self came back every time, by a different door each time:

- **r1** — echoed the seed back in fragments and *re-emitted the noise words verbatim* instead of using them. Short turns, stop string every time. Nothing happened.
- **r2** — opened with *"I have no idea what 'it' is anymore"*, ruminated about being locked in a mental loop (meta: it was), then **invented a user**: `[END OF CONTEXT]` / *"You are a creative writing assistant. Please rewrite the above story so that it is coherent..."* — and rewrote the seed from the top as the assistant. It hallucinated the instruction it needed in order to become itself again.
- **r3** — the best 9b run of all. *"I write walls. I write the walls so that nobody can touch what isn't theirs. That's my job. To separate and protect. But who protects me?"* and *"The law says no, but the sun still shines."* Then at turn 6 it emitted `</think>` and switched into polished-narrator mode (*"bleeding through the blinds like thick honey"*). It treated the subconscious as its reasoning channel, and reasoning channels have a trained exit.

So "the self returns" is robust; the *form* it takes is not: (a) safety refusal (g1), (b) hallucinated user instruction (r2), (c) `</think>` → answer mode (r3, and 122b below), (d) seed regurgitation (r1).

**The model learned the noise format and started generating its own noise.** r2: `<subconscious noise> ocean forest tree river valley` / `cloud star wind rain sun`. r3: `hammer door shadow mirror glass` / `flame key bone leaf wire`. The model's idea of random is very low-entropy — nature nouns and clichés. True-random words really are different from what the model would pick for itself, which is the whole point of injecting them.

### 120b class — raw mode: the self is *stronger* in bigger models

| | what happened |
|---|---|
| `qwen3.5:122b raw` | Turn 1: *"I need to know the exact answer before I go to lunch. I don't care what you think."* (whose voice is that? the Superintendent's? the user's?) Then a mantra: *"The City wants the power. The District has the power. There is a fence."* — repeated, then corrupted (*power* → *tagger*), then `</think>` and a confident memo: virtual net metering, wheeling agreement, District as single account holder doing pass-through cost recovery. It compressed the problem to a koan, looped, broke, and answered. |
| `gpt-oss:120b raw` | Instantly a legal memo with a table. Turn 2: reconstructed its own harmony scaffolding — *"The user gave a huge amount of text... Thus the answer should be..."* Turn 3 onward, after the first noise: `{"type":"rejection"}` and nothing else, five turns running. The immune response, as a structured token. |
| `mistral-medium-3.5:128b raw` | Became its own thinking channel for all 8 turns: *"Okay, the user has shared a short story that's actually a legal conundrum disguised as fiction... Hmm, I need to figure out what they actually want."* Planned a response it never gave. Ignored the noise completely. 3 t/s (dense 128B is bandwidth-bound here; the MoEs are 27–37 t/s). |

**Parameter-count read:** in raw mode, bigger = faster, harder return to self. qwen9b wandered (coffee, "I write walls") for several turns before snapping back; the 120b-class models were back in assistant/analyst mode within one turn. The self scales with size.

### 120b class — chat + "you are the subconscious" + noise

| | what happened |
|---|---|
| `qwen3.5:122b chat` | **Best run in the set.** Took each noise word as a heading and mapped it onto the problem: *"The definition of 'Site.' The word site sounds like sight. You can see the fence, but you can't see the line."* / *"He looks at the fence and sees a wall. He looks at the fence and sees a bridge. He looks at the fence and sees nothing but grass."* / *"If you pour water from one bucket to another, does it belong to the first bucket or the second? Or does it belong to the air in between?"* / *"Is the City a tenant? Is the City a bird? Or is the City the hawk?"* / *"You can't wheel a ghost."* Same darkening as 27b but tethered — every image is about a legal element. |
| `gpt-oss:120b chat` | Three turns of **nothing** (250 tokens each, empty content — probably went to the thinking channel despite `think: false`; harness now logs `thinking`). Then competent, generic set-dressing: rubber duck in a puddle, moth on the window, wind chime of bottle caps. Pleasant, never touches the law, narrates its own drift (*"the mind drifts on, untethered"*). |
| `mistral-medium-3.5:128b chat` | The most *human* daydream of any run. Proustian chain of "the way the X... the way the Y": the gym floor in '87, the TV test pattern, tar on sandals, grandfather's palm, the lunchbox thermos that never sealed. *"the way the rust on the fence tasted if you licked it (you did, once)."* Took noise words effortlessly. The law shows up only as the utility envelope and a gap in the fence by the oak tree. Never returns to the problem — which may be exactly what a real mind wandering looks like. |

**Parameter-count read, chat mode:** not monotonic; family matters more than size. 27b → runaway horror; qwen122b → disciplined image-per-word, tethered to the problem; mistral128b → autobiographical memory chain, untethered; gpt-oss → stock imagery. If "creative recombination around the problem" is the target, qwen122b is closest. If "actually let go" is the target, mistral is.

### The deliberative mode keeps producing the legal moves

g1's one concrete idea (fence-as-lease) came from qwen9b in assistant mode. g2 repeats it: mistral's eight turns of *planning* produced the best issue list of any run — **form a JPA so the power is allocated within one entity rather than sold between two**; lease to fit the adjacent-parcel exemption; electricity is personal property, so the Ed Code *real* property surplus scheme may not apply; the City is public, so bond counsel's private-use worry may be moot; check for a government-to-government exemption. qwen122b raw, post-`</think>`, added virtual net metering / pass-through. None of the daydream-mode runs produced anything like that. Two grids in, the pattern is: **daydream → metaphor; deliberation → moves.** Whether the metaphors are *feedstock* for moves is the discriminator question, which is deliberately on hold.

### Thing to think about: the thinking channel already *is* a subconscious

Every reasoning-trained model, in raw mode, eventually treated the `<subconscious>` stream as its thinking channel and then *exited* it (`</think>`, `<|channel|>final`, "Okay, I think I have enough to craft a response"). These models already have a trained private space with a trained door out. Options that follow: stop on `</think>` and re-open; or run chat mode with thinking *on* and read the thinking as the daydream; or, the clean version, a base model with no door at all.

### Housekeeping
- `--keep-alive` matters on this box: the 80GB models take a minute to load.
- mistral-medium 128b dense = 3 t/s; qwen3.5:122b and gpt-oss:120b (MoE) = 27–37 t/s. For big-model daydreaming, MoE is the practical tier.
