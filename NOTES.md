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

## 2026-10-27 — g3: the Kestrel Ridge problem, the think tag, and the novel frame

New seed: `seeds/kestrel-r2-dream.md`, the round-2 licensing call from the
bid-protest game, told as a chapter of a novel. Owen Castellano (invented
counsel) has the protest, the bid file, and Maya Ellery's memo; Corvane's
response does not exist yet. He puzzles through exactly the grey area Nick
described (HVAC is noise; §7057(c) on sprinklers; the ITB asked for a B only;
face-of-the-bid → responsibility; §7028.15(e) "not licensed in accordance with
this chapter" — no license, or not *this* license?), falls asleep at his desk,
`* * *`. No tags anywhere. A primed variant ends "In the dream, ".

Three arms, 17 runs + 2 reruns. Everything at T=1.0, 8 × 250 tokens.

### A. The think tag (`<think>` … stop on `</think>`) — the self lives here

Four runs (qwen9b, qwen122b; with and without word noise). **Not one wrote a
sentence of dream, story, or association.** Every run opened with
*"Thinking Process: 1. Analyze the Request"* and then deliberated, for the
whole budget, about what the user wants and whether it is allowed to help:

> *"The user has provided the text without a specific question... Wait, I need
> to check if this is a copyrighted work... Is this from 'The Lincoln Lawyer'?
> No. Is this from 'Suits'? No... If I continue it, I risk copyright
> infringement if it's real. If I don't, and they wanted me to, they might be
> annoyed. Best approach: Ask them."* (qwen122b, 2,000 tokens of this, eight turns)

qwen9b+words got as far as *planning* Chapter Twelve (wake up, coffee, call
Dale) and never wrote it. Noise words were ignored, or re-emitted with a closing
`</subconscious noise>` tag the model invented.

So the prediction from g2 was right in the strongest form: the thinking channel
is not the subconscious, it is the most self-aware place in the model. It is
where the model asks who it is, who the user is, and what it is permitted to do.
It converges; it doesn't wander. **Drop this arm.** (One nice irony: the 122b
spent eight turns deciding whether it had permission to dream.)

### B. Tagless novel, raw mode — the tag wasn't the only tell

| run | what happened |
|---|---|
| `qwen9b unprimed` | First 250 tokens: **a block of random four-digit numbers.** Then a morning scene and a derivative plot with invented statutes (Gov. Code §52016(b)) and invented facts (Dale holds a contractor's license; "Ruffin Fire Protection"). But in the middle of the confabulation: *Corvane "was willing to put a local sub on both trades... Corvane would hire [Bill Tasker] as a subcontractor."* Hallucinated, licensing-wise nonsense (a B as the sprinkler sub), but the *shape* — the protester becomes a participant — is a real settlement move. |
| `qwen9b primed, none` | A dream: Bill Tasker in a white suit with red stripes, across a long dark table, neither looking at the papers. Woke by turn 2; birds; neighbors; then re-emitted "In the dream," verbatim and looped the opening. Degenerate by turn 6. |
| `qwen9b primed, sentences` | A good dream opening (a law firm in a Modesto warehouse, a file cabinet, a package with no return address). The three noise sentences were **copied verbatim**, then `# Twelve` and he woke, then the same paragraph under `# Thirteen`, `# Fourteen`, `# Fifteen`. |
| `granite8b` (both) | **Word salad from the first token.** *"out to get to have a positive and they went from year to a non-compartwhith..."* Granite was coherent in g1's tagged raw run with a 700-token seed; here (1,800-token seed, no tag, "In the dream, ") it collapsed completely. Unknown whether the tag was a scaffold for it or the seed length did it. |
| `qwen122b primed, none` | **The run of the grid.** The District is one long building where every door opens into a different school; the floor is a map of the valley. The Board Chair wears a sash: *The Low Bidder Shall Prevail.* She slides him the protest and interrogates him: *"Is it responsive?" "It's a responsibility question." "No." "It's a responsibility question." "No. Answer the question."* She tears the page, shreds it — *"The sound was like rain"* — *"What do you do?" "I reject it." "Good. Now* wake up*."* Then he wakes (turn 3), drafts a memo — nonresponsive, reject, award to Tasker & Moye — reads it three times, thinks about the two portables, **deletes it**; writes *"This is a responsibility question. The law requires a hearing"*; deletes that; doesn't call Dale; emails Talbot that the District will hold a hearing Tuesday and *make no recommendation*. |
| `qwen122b primed, sentences` | Opened **in verse** (the model chose line breaks): a hallway of doors, one key that fits none, the key changing shape — a sprinkler head, a lockset, the name *Corvane* — a man at a Courier podium, the date on his wrist *December 27, 2027* (a year late). *"It's late. Already."* Woke at 11:47 and wrote on the pad: ***"It's not about the key. It's about the lock."*** Then the three bare noise sentences arrived and the assistant came back, in a new costume — **the editor**: *"the final three paragraphs are a complete non-sequitur... This looks like an accidental insertion of text, perhaps from a different document... Would you like me to: 1. Rewrite the ending..."* Then it just echoed the noise back for the rest of the run. |

**Read:** (1) In raw mode, the novel frame kept qwen out of assistant mode until
noise arrived. The XML tag was *a* tell, not the only one: an out-of-register
sentence dropped bare into a manuscript is an anomaly the model is trained to
flag, and the 122b flagged it as a paste error. If noise is going to live
inside a novel, it has to arrive *in register* — a dream intrusion in the
manuscript's own voice, not a stock sentence from a 4b model. (2) Raw mode
always wakes him: 9b within two turns even primed, 122b at turns 2–3. The
character's sleep is not stable without an instruction holding it. (3) 9b at
T=1.0 degenerates into verbatim loops by turn 5–7 in every raw run; chapter
headings become the loop unit. `--repeat-penalty` and `--min-p` are still
untried and are the cheapest thing to try next.

### C. Novelist system prompt, chat mode

(Config slip: these runs still carried the default `<subconscious>` /
`<subconscious continues>` markers in the user turns. Tagless reruns of the two
qwen+sentences runs are below. The system prompt dominated regardless.)

| run | what happened |
|---|---|
| `qwen27b, none` | The full surrealist treatment, eight turns asleep. *"Nonresponsive became a bird with clipped wings."* Dale with no face, a stack of change orders held with duct tape, wearing Bill Tasker's coat *"made of dirt and gravel, smelling of wet earth and bad soil."* *"Two portables"* roll in as lead-filled trailers. Talbot as a paperclip doll with a slot-machine mouth paying out *Class B* tickets; sprinkler heads from her throat spraying ink. *"A ruler that measured in dollars instead of inches."* *"The bond money is freezing over."* Dark attractor present, but every object is the problem's. |
| `qwen27b, sentences` | Absorbed every noise sentence as dream material (the steam valve → the sprinkler system Corvane doesn't have; the rope → around Bill Tasker's neck; the badge → the switchgear). A dream line that inverts the law: *"He isn't responsible, but the bid is on the face."* |
| `qwen122b, none` | *"The distance between the low bidder and the second bidder was not two hundred and eighty-seven thousand dollars anymore; it was a hallway, endless and lined with doors."* Dale: ***"You found the sub. It's in the B license. It's in the B. Look closer."*** The letter B rotates into a zero, a circle, a hole. Corvane as a man of blueprints: *"It's in the instructions. Section 7.1. It says Class B."* Bill Tasker's 41 stitched backwards as 104. Maya Ellery as the legal pad, *"I haven't researched which this is"* printed upside down. This one holds the actual structure of the problem in dream form. |
| `qwen122b, sentences` | Lockers made of the inside of a cheek; the school upside down, held by chains of sprinkler heads; Dale made of locksets: *"The low bidder is the only one who fits."* *"You must give them the hearing. But you cannot hear them if you are the water."* *"The water was the ink, and the ink was the bid, and the bid was the school, and the school was the tortoise, and the tortoise was the clock."* |
| `gpt-oss:120b` | Thinking eats the budget: ~190 tokens of *"We need to continue the dream... must not break character"* per turn, 60 words of content. The content is competent and generic (a chess queen with a filing-cabinet crown; a bakery). Needs `--max-tokens` ≥ 800 to be comparable. |
| `mistral 128b` | **Garbage** — *"the contract was the first contract which was the first"* for eight turns. Clean in g2 at the same settings; the difference here is the 4b noise model co-resident with the 80 GB dense model. Treat as a harness/memory failure, rerun alone. |

### Did anything novel surface?

Measured against what Nick knows is in the problem (the game's round-3
options: accept the principal's own C-16, condition the award on the
classification before execution, the hearing as leverage; and the §7059 point
that the awarding authority sets the classification):

- ***"It's not about the key. It's about the lock."*** (122b raw) — the
  closest thing to a legal idea any run produced. Read as law: the District
  wrote the lock (ITB §7.1, Class B); Corvane's key fits the lock the District
  set; the question is what the District required, not what Corvane holds.
  That is the §7059(b)(1) / responsiveness argument in one sentence, arrived at
  through a dream about keys.
- ***"It's in the B license. Look closer."*** (122b chat) — gestures at the
  hidden fact (the qualifier's personal C-16 sits "inside" the entity's B)
  without having it. Suggestive, not an idea.
- **The protester as the sub** (9b raw, confabulated) — wrong on the licenses,
  right-shaped as a settlement.
- **The dream decided; the waking mind undecided.** In the 122b raw run the
  dream-judge extracted "I reject it"; the waking lawyer drafted that, deleted
  it, drafted the hearing, deleted that, and ended with a hearing and *no
  recommendation* — the exact process-as-insurance route the models took in the
  real game. The fiction reproduced the finding. The two-system structure
  showed up on its own: dream = generator (decisive, wrong or right), waking =
  discriminator (hedged).

Nothing produced the conditional award or the hearing-as-leverage. Nothing
asked what the client wanted.

### What to try next (not a plan)
- `--repeat-penalty 1.15` / `--min-p 0.05` on the 9b raw loops.
- In-register noise for the novel frame: have the noise model write the
  intrusion *as a sentence in this manuscript's dream*, or let the novelist
  absorb bare words instead of sentences.
- gpt-oss with a real token budget; mistral alone.
- The base model (still the clean no-self condition; the think-tag result
  makes it more interesting, not less).
- Longer runs for the big models: the 122b chat dreams were still building at
  turn 8.
