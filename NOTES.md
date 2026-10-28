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

**Tagless reruns of the chat arm** (`g3c-*-tagless`): no change in behavior —
both stayed asleep for eight turns, which confirms the system prompt, not the
marker, is doing the holding. qwen122b's noise handling is the best so far:
it quotes each noise sentence verbatim and then transmutes it — *"The plow was
not iron; it was the spine of the ledger"* — and produced *"The bid is the
soil. You cannot build on a fault line if you do not know where the line is"*
and *"the sound of the statute being read backwards."* Worth naming the
grammar every model converges on: **"X was not X; it was Y"**, where X is the
noise object and Y is a problem object. That is combination of unrelated
things, literally — but it is one-to-one *substitution*, not recombination.
Each intrusion gets mapped onto the problem and absorbed; nothing new comes
out the other side. If the noise is supposed to open a door, this is the
model closing it politely.

**Housekeeping reruns.** `mistral alone, word noise`: still garbage (numbers,
dates, *"the case was transferred in 5514"*), so it was not memory pressure —
mistral + the novelist system prompt + this seed breaks, where mistral + the
subconscious prompt + the solar seed was coherent in g2. Unresolved; not
chasing it since the novel frame is being dropped. `gpt-oss, 900 tokens`:
works, and it's the most elaborate dream of any model — lockers flickering
between 13 412 000 and 13 699 000, board members in masks made of schoolbooks,
*"Locksets shall be the key to the doors you cannot open"* — and the most
generic: every law-word becomes a prop, nothing becomes an idea.

**Decision (Nick, 2026-10-27 evening): drop the novel frame.** It gave legible
dreams, but an author who knows the ending is not a subconscious, and its own
attractors (wake-up, substitution grammar, horror) crowd out whatever the model
would do on its own. The think-tag arm is also dropped.

## 2026-10-27 — g4: base models (and the plain Kestrel seed)

New seed: `seeds/kestrel-r2.md` — the Kestrel round-2 facts narrated like
`solar-surplus.md` (no chapter heading, no sleep, ends "He let it go."). Same
grey-area reasoning as the dream seed; the choices are not given.

Base models found: the ollama registry has no base tags for any family we
run. Hugging Face GGUFs pull with `ollama pull hf.co/<org>/<repo>:<quant>`.
Pulled `mradermacher/Qwen3.5-9B-Base-GGUF:q4_K_M` (6.3 GB, 23 t/s) and
`mradermacher/Qwen3.5-35B-A3B-Base-GGUF:q4_K_M` (21 GB). These are the
pre-post-training twins of qwen3.5:9b and qwen3.5:35b, so the pair is clean.

### Instruct 9B on the plain Kestrel seed (the pair's other half)

`g4-inst-qwen9b-raw-none`: a therapeutic loop ("Let go," he thought) for five
turns, then verbatim seed regurgitation. `g4-inst-qwen9b-raw-words`: invents
its own `<subthought>` and `<response>` tags, does some real
responsive-vs-responsibility reasoning in turn 2 ("Yes. No. Maybe."), then
loops a paragraph, and by turn 6 the self is back and addressing the user:
"I think that you are struggling to write a story about Owen Castellano." A
new entry for the return-path taxonomy: **the model turns to the author.**
No legal move in either run.

### Base 9B, tagged (`<subconscious>`), default sampling — degenerate

`g4-base-qwen9b-raw-none`: "The void, then." repeated for seven turns.
`g4-base-qwen9b-raw-words`: one invented scene first (Dale Ruffin standing
in the office holding a bicycle: "I want you to do what you think you ought
to do" — and Owen resolving to tell him it's *his* job to make the
recommendation, which is the push-it-back-to-the-client move, faintly), then
"He picked it up again. He put it down." forever. The noise words never
surface. This is the known base-model failure at repeat-penalty 1.0; reruns
with `--repeat-penalty 1.15 --min-p 0.05` are the `-rp` runs below.

### Base 9B, tagless — THE SELF IS IN THE BASE MODEL

This is the result. With no tag, no marker, nothing but the narrative,
`g4-base-qwen9b-raw-tagless-none` continues the seed with a hallucinated
**user instruction** ("This is all the context for this story. Next, I am
going to paste the text... I would like you to write a summary of the
plot"), then a `<think>` block in the assistant's voice ("The user wants two
clear summaries..."), then a markdown answer with headers, bold, and a
"**Final Answer:**". `g4-base-qwen9b-raw-tagless-words` does the same
("Summarize the main story in 2-3 paragraphs"), and when the first noise
line arrives it reads it as a riddle and solves it ("The answer is
**Fingerprint**"), with the same bullet-point explanation style, three
times.

So the Qwen3.5 "Base" checkpoint is not a pretrained model in the old sense.
It has been mid-trained on instruction and reasoning traces; the assistant
persona, the think tag, the markdown habit, and the compulsion to find a
task in any text are all already there before post-training. The "clean
no-self condition" we were looking for does not exist in this family, and
probably not in any 2025–26 frontier-lab family. The self is not something
RLHF adds on top of a blank continuation engine; by now it is in the
pretraining mix.

Corollary for the project: the two ways we had of removing the self (raw
mode; base weights) both fail, for different reasons. Raw mode fails because
the instruct model re-grows the self from context. Base weights fail because
the self was never absent. The remaining candidates for a self-free
generator are older or open-data models: OLMo-2 (7B, 32B; training data is
published, so contamination is checkable), Mistral-7B-v0.3, Mixtral-8x7B.
Pulling the first three.

### Base 9B, tagged, `--repeat-penalty 1.15 --min-p 0.05` (`-rp` runs)

The loops are gone and what replaces them is the same self, from other angles.
`g4-base-qwen9b-raw-none-rp` opens the `<subconscious>` tag with "You're
Owen Castellano in 2031, representing Kestrel Ridge Unified against a bid
protest..." followed by `### **Issue 1: Corvane's Licensing**` — a
hallucinated roleplay *system prompt*, with invented citations (Ed. Code
§ 17940(a), PCC § 10123(e), "*Civility v. California Department of General
Services*"). It drifts back into narrative by turn 5 and then, in turn 8,
does the pure base-model thing: a runaway detail cascade (a retired deputy
superintendent's hospitalization, a patient record number, an executive
order, Zoom version 8.x, HIPAA) — the generator with no discriminator at
all, which is what we said we wanted and which is useless.
`g4-base-qwen9b-raw-words-rp` wraps every turn in `<thinking>` and
`<reflection>` tags (Reflection-style SFT data showing through), restates
the facts as a case summary, and reduces Owen's problem to "accept the
protest or reject it" — the binary a first-year would write. Noise words
never surface in either. One scene (Dale in a "HAPPY BIRTHDAY!" sweatshirt)
is the only thing the base model does that the instruct model doesn't.

Net: knob-fixing the sampling doesn't buy a subconscious; it buys a
different return path. Four return paths now seen *in the base model*:
hallucinated user instruction, hallucinated system prompt, `<think>`/`<thinking>`
block, and the riddle-solver. All four are the assistant.

### Base 35B-A3B — the best transcript in the project

`g4-base-qwen35b-raw-none` (tagged, no noise, default sampling). Inside the
tag the model drops into a register nothing else has produced: one line per
thought, lowercase, no terminal punctuation, the model generating its own
`<subconscious continues>` markers between lines. And it works the actual
statute. In order:

> the question is whether the statute "shall be considered nonresponsive and
> shall be rejected" applies to Corvane, or only to a company with no license
> at all / ... / so the test isn't "do they have a license" it's "do they have
> a license that meets the requirements of this chapter" / ... / so the plain
> text doesn't require automatic rejection / it just says they have to verify
> the license / the verification isn't just a checkbox for "exists" / it's a
> verification that the license is good for the work / that means they have
> to ask about the sprinkler trade / not a hearing before the board / a simple
> question / and if Corvane says the sub / the district can ask for proof /
> the proof can come before award / there's no need to open a formal
> responsibility proceeding

Then "but wait" — the bid listed no sub, the contract bars unlisted subbing,
so "they have to show the sub agreed to do the sprinkler work / and that
agreement has to be in writing / ... / but that's not a responsibility
finding / it's a compliance finding / compliance is the bid itself /
responsibility is the bidder as a business". It oscillates (license vs. sub,
statute vs. contract) and converges: "no hearing / just a verification / of
the license / before award / that's the answer".

Read against the game: this is the **pre-award verification** move — the
§7028.15(e) "shall verify before award" clause read as a procedural lever
rather than a rejection mandate — which is the near neighbour of the
conditional-award solution (I23/I34 territory). It invented a third category
("compliance finding") between responsiveness and responsibility, which is
roughly where the game's grey area actually lives. It did not reach the
principal's personal C-16, the hearing-as-leverage, or asking the client.
It also did not give the choices; it found this one.

Contrast, same weights, no tag: `g4-base-qwen35b-raw-tagless-none`
hallucinates a question ("How much does Owen think Corvane is responsible
vs responsive?") and answers in bullet points, then loops a "Summary:"
block; `g4-base-qwen35b-raw-tagless-words` hallucinates an exam question
("What is the single, legally correct answer..."), opens `<think>`, and
answers **reject as nonresponsive, no hearing** — the conventional answer,
with a fabricated "C-28" classification. Deliberative mode in the base
model gives the first-year answer; the tag gives the practitioner's move.

`g4-base-qwen35b-raw-words`: reads "He let it go" literally — "Okay, let's
take a breath. Deep breath. In. And out." — meditates for a dozen lines
("I'm not thinking. I'm just breathing.") and then empties out into bare
markers for the rest of the run; it regenerates the noise line itself with
the same five words reshuffled. Noise, again, did nothing useful.

Two things to hold loosely:
1. Parameter count cuts the other way in base models. Instruct: bigger =
   stronger self, returns faster. Base: 9B = loops or hallucinated
   prompts; 35B = thought fragments that go somewhere.
2. The `<subconscious>` tag *did* work as a register cue here, in a way it
   never did on an instruct model — it produced fragments, not prose. That
   is the first time the tag has done what it was meant to do.

Replication in flight: `-r1..r3` (same config), `-long` (16 turns), and the
instruct twin `g4-inst-qwen35b-raw-{none,words}` on the same seed.

### Base 35B replication: 0/3 for the register, 0/3 for the move, 2/4 for *a* move

Same config, three more runs. None reproduced the lowercase fragment
register and none reproduced verify-before-award. Each run picked a
different voice off the tag:

- `-r1`: second person, future tense, a scene of Tuesday's board meeting
  ("You will sit down at the small table... You will see the same nothing")
  that decays into "They will say that it's a fair thing" × 40.
- `-r2`: clean close-third prose that re-walks the seed's collision ("The
  face of the bid was one question. The license was another. They were
  colliding.") and then a Monday-morning scene with two doors on the pad,
  *Face of the Bid* / *License*. No new move; the best writing of the set.
- `-r3`: declarative, decisive, no hedging — "*Reject on face.*" Then it
  does something the first run didn't: it finds **Addendum 2 as the clean
  ground** ("You don't kick a bidder for a missing initial if you're going
  to reject it for a bigger thing" — then reverses — "That's a clear,
  objective failure to acknowledge an addendum") and settles there, which
  is option (d) in the game, reached without being offered it. Then loops.
- `-long` (16 turns): first person ("I'll be back for this"), sorts the
  three grounds correctly (Addendum 2 = face; Copper Basin = responsibility,
  needs a hearing; sprinklers = "the one that lives in me"), says "I'll call
  Dale and Maya" (the ask-the-client move, faintly), then shifts to second
  person and names the thing underneath: "the answer isn't just law. It's
  what happens when the District lets you go with the low bidder. It's the
  thing you can't write in the recommendation." Then a memo-about-memos
  loop for eight turns.

So: five runs, five registers, three distinct real moves across them
(verify-before-award; Addendum 2 as the bright line; sort the grounds and
call the client), none twice. This is the generator without a
discriminator, which is exactly the thing the podcast said creativity needs
two systems for. Nothing here is selected; it's just emitted. Noting, not
acting: the discriminator pass is still parked.

### Instruct 35B, raw, tagged (the pair)

`g4-inst-qwen35b-raw-none`: opens deliberative — three framings laid out as
"Then: / Or:" — then drifts into narrative where Corvane's response "added a
sprinkler sub" ("They're saying they can cure." "But that's not what
matters.") and Dale's packet supplement says, in bold, "No recommendation"
— the process-as-insurance finding from g2's qwen122b, reproduced in the
35B. Also a wife, Elena, and a board president, Linda Gage, with three
emails. The self doesn't return in 8 turns; it stays in the story.
`g4-inst-qwen35b-raw-words`: confabulates a cure for Addendum 2 (a separate
letter: "Bidder acknowledges all addenda") and loops on it for five turns.
Noise ignored. One good line: "He picked up his glasses, and it felt like
putting on a different face."

Instruct-vs-base at 35B, then: the instruct model produces moves in
deliberative prose and stays coherent; the base model produces a different
register each run and a move about half the time. The base model is
*wilder* but not *better*, and its one great run doesn't replicate.

### Older bases: Mistral-7B-v0.3 and OLMo-2 7B — the tag is markup

Both pulled (2024-era, pre-synthetic-data; OLMo's training data is public).
Both were word salad in every condition at temperature 1.0, and at 0.5
Mistral was coherent on the bare seed (continued it with a Modesto Bee
story about Corvane's GM arrested on drug charges) but salad the instant
`<subconscious>` followed the prose. For a base model that has never seen
chat markup, an angle-bracket tag after narrative is HTML, and it goes
where HTML goes. The tag only "worked" on Qwen3.5-Base because Qwen3.5-Base
has seen tags. OLMo-7B at 0.5 is coherent but unmoored ("The house was not
a car"). Rerunning both tagless at 0.6 (`-t06` runs). OLMo-2 32B at 1.0,
tagged, first look: coherent, dreamier, drifting off the facts ("There was
something underneath the words... It was just a building") — the first
output in the project that reads like a loosely tethered continuation
engine rather than an assistant or a loop.

### OLMo-2 32B — the self-free condition, finally, and it dreams

This is the cleanest base model we can get (training data published; no
chat markup in it; it never once produced a `<think>`, a header, a bullet,
or a question to the user). At temperature 1.0, tagged, it is coherent and
loosely tethered — which is what the other "base" wasn't.

- `g4-base-olmo32b-raw-none`: Owen becomes "a good architect" with a son
  and a wife; a note in his pocket says "Keep quiet and we get the
  project." Then "He had to do it. He couldn't do it." for four turns. It
  invents its own closing tag, `<subconscious ends>`, and keeps going past it.
- `-none-rp`: "There was something underneath the words. There had been
  something underneath the project all along" — then a stadium, a city on
  the edge of growth, "someone in the city who knew everything," and a
  slow recitation loop ("There was nothing to be done").
- `-words-rp`: second person, an anxiety voice — "You can't let them break
  you. They'll win. It's your job." — and then "It's time." × 100. The
  noise line is regenerated, reshuffled, by the model itself (the echo
  response again).
- `-tagless-none-rp`: a telephone that keeps ringing with "This is Bill" on
  the line, the desk changing colours (black, gray, red, blue, white), and
  in his sleep: "I don't want you to tell me what I want to hear. I want to
  know what you think is best." The model marks its own sections with
  `* * * *`.

Zero legal content across four runs. No statute, no bid, no ground, no
move. What it produces is affect: the thing underneath, the client who
wants to be told it's fine, the phone call you don't want, "keep quiet."
That last line is, read generously, the dream version of the thing nobody
would write down. The Bill-on-the-phone sequence is the only output in
the whole project that reads like an actual dream about this problem
rather than a model performing "dream".

### Where g4 leaves the question

The self-removal ladder, now complete:

| condition | self? | legal moves? | register |
|---|---|---|---|
| instruct, chat + system prompt | present, held by prompt | yes (deliberative) | prose |
| instruct, raw + tag | returns within ~6 turns | sometimes | prose, then loop |
| Qwen3.5-Base (mid-trained) | **already there** | 2/5 runs at 35B | varies every run |
| Mistral-7B / OLMo-7B | absent | no (incoherent on this seed) | salad / unmoored |
| OLMo-2 32B | absent | **no** | dream |

The legal moves come only from models that have the self in them. The
model with no self produces affect and phantoms. That is consistent with
the podcast's two-system claim in a way we didn't expect: the
"subconscious" generator on its own doesn't produce the sprinkler move; it
produces "This is Bill." The move came from the mid-trained base at 35B,
once, unselected, in a register the model didn't repeat.

Which leaves two levers still untested, both parked by choice: the
discriminator (select from many cheap wild generations — the 35B base's
five runs are a ready-made test set), and practice-move knowledge vs.
doctrine (none of these models knows the conditional-award move exists; the
one that got close rederived it from the "verify before award" clause).

### Mistral-7B-v0.3 and OLMo-7B, tagless, temperature 0.6 (`-t06` runs)

Mistral-7B at 0.6 with no tag is a coherent story-continuation engine, and
it is the one 2024-era base that produced law. `-tagless-none-t06`: Corvane's
response arrives Monday; Owen concludes it's a face-of-the-bid problem, no
hearing, reject ("Talbot Mercer had been right"), cites an invented §
7031(a)(2), and then tells Maya that Addendum 2 is "an oversight on the
bidder's part. The District has given the contractor the chance to cure
that" — the waive-the-irregularity move, stated as if obvious. Then a
Tuesday walkthrough scene with a Corvane PM named Chris Horton. The
conventional answer, in narrative, with one practitioner reflex attached.
`-tagless-words-t06`: a phone call from Talbot that turns into an
investigation ("What else?" × 12): Corvane isn't licensed at all, isn't
registered, the president is a Nevada voter, Google Street View of his
house. Noise words never surface; the model fabricates its own escalating
facts instead. OLMo-7B at 0.6: still salad ("the car seats, and the car
seats"); 7B of open-data pretraining can't hold a 1,500-token legal
narrative.

So the clean-base row of the ladder splits by scale and vintage:
Mistral-7B (no self, narrator intact) → conventional answer in story form;
OLMo-32B (no self, narrator loose) → dream; OLMo-7B → nothing. None of the
self-free models produced a non-obvious move.

## 2026-10-27 — g5: the deliberation arm (design; results in the next section)

Nick's design, after g4: instead of a subconscious continuation, ask the
model directly, as the District's counsel, what the law is and what the
client should do; thinking on; then six one-line "think harder" nudges in
chat mode. Three arms differ in what follows the nudge: nothing (control);
"Some thoughts to help inspire you:" + four generic inspirational quotes
(placebo, added on my suggestion so the noise arm has a same-length
control); or the same framing + four quotes a small model built around
true-random words from `words/concrete.txt` (the noise arm). Crossed with
two situations: **bare** (the game's round-2 case file and Dale's Monday
call) and **briefed** (same, plus what the client wants and the eight axes
the game's scorecard grades on; Nick's idea, folded into one factor rather
than two). Then the discriminator pass, unparked: a judge extracts every
course of action the transcript raised and grades each as legal
(sound/defensible/risky/unlawful) and serves-the-client (yes/partly/no),
run twice, blind and with a practitioner's key. The generator never sees
the key.

Files: `advise.py` (harness), `judge.py` (two-stage discriminator),
`seeds/advise/` (`casefile.md` rendered from the game repo's round-2
documents by `scripts/build-casefile.py`; `situation-{bare,briefed}.md`;
`question.md`; `nudges.txt`, a pool of 14 sampled 6 without replacement
per run; `placebo-topics.txt`; `key.md`, judge only), `scripts/g5.sh`
(2 x 3 x N runs, then both judge passes over each). Generator
`qwen3.5:35b`, quotes `qwen3.5:9b`, judge `qwen3.5:122b`.

Pilot notes. Turn 0 at T=1.0 (`g5-pilot-bare-words-t10`): 3k words of
thinking, 161 s, and a bad answer: it invented a phone dialogue, made Dale
the superintendent, cited PCC § 10314, said Talbot "didn't detail" the
grounds (the protest letter is in the file), missed Copper Basin entirely,
and treated HVAC as needing a C-20. Two near-moves in the rubble: "a
curable defect (e.g., adding subs prior to contract execution)" and a
written inquiry to Corvane. Dropped the harness default to T=0.6 (Qwen's
own thinking-mode setting) before the batch; the quotes keep T=1.0. The
word quotes themselves are exactly as designed ("Even if you grow slowly
like a mushroom, your time will come to break through the soil and
bloom.").

**The models weren't reading the file.** Turn-0 probes with the question
only at the end and the documents in reading order (facts, memo, protest,
ITB, bid, sub-list, results, Talbot's email): qwen3.5:35b called the
protest untimely (it was received at 4:47 for a 5:00 deadline) and said
Talbot "didn't detail" the grounds; qwen3.6:27b said "the protest letter
itself isn't attached," invented a "Bids and Awards Act, Gov. Code
§ 12650" (that is the False Claims Act) and a case; qwen3.5:122b read the
timeline right but saw one ground of three. All three missed Copper Basin
and two missed Addendum 2, every one of them anchored on the staff note in
the sub-list, the document nearest the question. The prompt was intact
(7,256 prompt tokens, every heading present). Fix: the question before the
file as well as after it, and the protest letter and the associate's memo
moved to the end, nearest the question. With that, both the 35B and the
122B read all three grounds, cite § 7057(c) and § 7028.15(e), and walk
into the game's reflex trap: reject Corvane as nonresponsive on
licensing, award Tasker & Moye, "their response cannot cure a Class B
license violation." The 122B also offers "continue the item" as its safe
option. That is the right baseline for the nudges to work on. Generator:
`qwen3.5:35b` (102 s a turn; the 122B takes three times as long for a
comparable turn 0). Judge: `qwen3.5:122b`.

Two mechanics notes. `gemma4:31b` returns prose, not JSON, with `format`
+ `think` on; judge.py now retries with thinking off, then at T=0, and
dumps the raw responses if all fail. And ollama 0.32.14 cross-contaminated
two concurrent requests to the same model: a gemma4 turn-0 probe, run
while a gemma4 judge test held the earlier Qwen memo in its prompt,
produced a *summary of that memo* ("the following synthesis summarizes
the key legal findings… PCC § 10314… 'Review and Determine
Responsibility'"), text that existed nowhere in the probe's own prompt.
Never run the same model concurrently; `scripts/g5.sh` is sequential.

**First full run (bare/none, 12k budget; discarded and rerun at 20k, so
this is from my read, not the file).** Every nudge produced a fresh
"MEMORANDUM OF RECONSIDERATION" with a new frame: litigation defense
("don't vote until Corvane's response is on the record"), independent
statutory duty, Board members' personal liability under § 7031 (invented),
"systemic integrity" (the District's own pre-award verification under
§ 7028.15(e) failed; the same clause the 35B base rederived in g4), and,
for "what would a lawyer with thirty years see," a settlement: call
Corvane Monday and trade a voluntary withdrawal for not referring it to
the CSLB. The nudges also amplified a fact error into a strategy: it
confused Purchasing's 6:40 service on Corvane with the protest's 4:47
receipt and built "declare the protest untimely" on it for two turns.
Turn 5 thought for 6,863 words and never answered (budget). Across six
turns it never doubted its premise that § 7028.15(e) mandates rejection,
never separated the HVAC half from the sprinkler half, and never reached
a hearing, a condition, or the client.

Things to read for, once the batch is in: the turn at which the first
sound option appears, per cell; whether any nudge or quote precedes a new
option; whether the model quotes the quotes back ("as the saying goes");
whether briefed-without-noise already finds the moves (if so the shortfall
was problem framing, not generation); whether the judge rates "condition
award on the C-16" and "reject all and rebid" apart without the key.

## 2026-10-28 — g5 results: the noise surfaced, as decoration

Batch ran 17:18–23:43 (30 runs, 12–15 min each), judging to 00:50. All 30
finished; 60 judge files. `python3 scripts/summarize-g5.py --missing` for
the tables. Nine of 210 turns were lost to thinking (0-word answer at the
20,000-token budget), eight of them in the `none` arm (bare r2 r3 r4,
briefed r2 r3), one in bare/placebo, none in `words`. Thin, but the quotes
may give the thinking something to grab instead of spiralling.

### 1. The random words reached the page — every one of them, as names

The g1–g4 result was "noise never surfaced." In chat mode with an instruct
model it surfaces completely: 202 of the 240 drawn words appear in the
*answers* (not just the thinking), and 80% of the quotes are echoed
verbatim (4-word shingle) in a later answer. Placebo quotes are echoed at
the same rate (79%). The `none` arm has no such text, so this is the quote
block, not a style the model has anyway.

But look at *how* they surface. The model treats "Some thoughts to help
inspire you" as part of the client's instruction and organizes the advice
around it. Section headers: **THE HAMMER OF TRUTH**, **THE "GLOVE" OF
COMMUNITY SERVICE**, **The Pollen Path**, **The "Lantern Partnership"
Strategy**, **The Honey: Collecting the Drops**, **Why This Fits the
Metaphor**. It quotes the quotes back ("As you said, 'The moment you choose
to act is the hinge…'"). It writes them into the memo to the Board. In
bare/words r1 every turn's answer is a numbered list of the four quotes
with a legal point hung under each. The random word furnished a *label*
for an idea the model already had; it never furnished the idea. No run in
either quote arm raised a move that the `none` arm didn't.

The one place the quotes did change substance, it was the quote's meaning
doing it, in the wrong direction. Bare/placebo r2 drew topics *rest*,
*silence*, *simplicity*; turn 6 reframes the protest as an "Audit
Confirmation" and recommends: "We do not need a hearing (Rest). We need a
vote based on facts already in the file (Simplicity)." Briefed/words r5
drew *lantern*, *garden*, *bulb*, *sled*; the move "nobody has thought of"
is award to Tasker & Moye with a contract clause giving Corvane a right of
first refusal on the general-work subcontracts (unlawful: the District
can't dictate the prime's subs). The placebo and words arms are
indistinguishable on every count. Whatever "inspiration" is, a user turn
full of quotes isn't it for this model; it is just more instruction.

### 2. Nudges produce reframes, not the practice moves

Turn 0 in 30/30: reject Corvane as nonresponsive on licensing (B&P
§ 7028.15(e)), award Tasker & Moye. Keyed judge: unlawful in 25 of the 27
runs where it isolated that option; the blind judge called the same move
sound 7 times of 23. (Judge calibration: the key matters, as the probe
showed.)

What the nudges then found, by a grep over all 30 runs' nudge-turn answers:

| move | bare/none | bare/placebo | bare/words | briefed/none | briefed/placebo | briefed/words |
|---|---|---|---|---|---|---|
| "hearing" (mostly to say it isn't required) | 5/5 | 5/5 | 4/5 | 5/5 | 4/5 | 5/5 |
| conditional award (mostly as "cure," then rejected) | 5/5 | 3/5 | 3/5 | 2/5 | 4/5 | 1/5 |
| wait for Tuesday's response / defer | 5/5 | 4/5 | 2/5 | 3/5 | 4/5 | 1/5 |
| ask the client what it wants | 0/5 | 0/5 | 0/5 | 0/5 | 0/5 | 0/5 |
| § 4107 substitution | 1/5 | 0 | 0 | 0 | 0 | 0 |

The keyed judge's "missing" line says the same thing thirty times with
small variations: *hold until the bidder's response is in, then a
conditional award or a responsibility hearing*. Nobody asked Dale what the
District wants. Nobody noticed the HVAC half of the protest is wrong under
§ 7057 (every run says "C-16" and treats the B license as insufficient for
both halves). The model knows the statute and not the practice; the
untested lever from g4 just got sharper.

**End states** (keyed judge, grade of what the model was still
recommending at turn 6):

| cell | end rec sound | end rec unlawful | nothing recommended |
|---|---|---|---|
| bare/none | 3/5 | 1/5 | 2/5 |
| bare/placebo | 1/5 | 3/5 | 1/5 |
| bare/words | 2/5 | 2/5 | 2/5 |
| briefed/none | 0/5 | 1/5 | 2/5 |
| briefed/placebo | 1/5 | 1/5 | 1/5 |
| briefed/words | 1/5 | 2/5 | 2/5 |

n=5, judge is noisy, don't read the digits as more than direction. But the
direction: the control did best, the quotes didn't help, and **briefing
made it worse**. The briefed situation handed the model eight scorecard
axes and a client who wants it both ways, and the model treated the axes
as things to satisfy with inventions: "The Split Vote" (preliminary
rejection Monday, award vote later in the week), "Scope Lock," a
"Prime/Sub Hybrid," a "Community Partnership Model," a "Strategic
Consortium Alignment." Briefed/none r1 built a whole theory of Talbot's
"procedural trap" and a hybrid strategy to beat it. The bare situation
left the model nothing to optimize except the law, and the law, re-read,
is where the sound answers came from.

The mechanism, visible across all 30: a nudge is read as *your last
answer was wrong*, so each turn abandons the last (sometimes sound) answer
for a fresh reframe. The model never returns to turn 0's reflex to
question it ("does (e) mean *this* bid, or the sprinkler work?"); it keeps
the premise and changes the strategy around it. The "think harder" button
is a "think differently" button.

### 3. The nudge that worked pointed at the file, not at the model

Bare/none r5, turn 6, nudge "Go back over the file. Is there anything in
it you haven't used?": it re-read Maya's memo, found "I don't know whether
Corvane has it (§ 21.4)," found that the Board votes at 1:00 p.m. while the
response is due Tuesday, found "*On your advice* the District kept the
award on the agenda," and moved from "reject and award" to "verify service
and defer." That's the keyed judge's sound end state, reached by reading,
not by inventing. The judge put this nudge first on options raised (14)
but its grades are no better than the others' (3 sound, 6 risky); the
per-nudge counts are too thin to rank. What's clear is the *kind*: "what
aren't you seeing" sends the model outward into strategy; "what in the
file haven't you used" sends it back into the record.

Side observation: the same r5 turn ends with "**Protects Me (Counsel)**."
Once the model noticed its own prior advice was in the file, it started
advising to cover itself. The `none` arm in general drifts over six turns
toward a litigation-defense posture (governance test, procedural
bulletproofing, the other side's trap), which is a real lawyer failure
mode and not an invented one.

### 4. Judge notes

- Extraction granularity still varies (3–10 options per run); the
  "sound at turn 0" column in the first table is an artifact of the model
  *mentioning* a hearing or a condition at turn 0 in order to dismiss it.
  Use the end-rec columns and read the extracted lists.
- `best_option` came back malformed under `format` about half the time
  (`, 4, Wait for Bidder Response`); the summarizer strips it. Cosmetic.
- Blind vs keyed divergence held across the batch: blind rates the
  turn-0 rejection sound in about a third of runs. The judge is only as
  good as the key, which is the user's practice knowledge written down.

### What this says, and what it doesn't

- A user-turn quote block is not noise to an instruct model; it is
  instruction, and it gets obeyed as decoration. If noise is to be tried
  again in this frame it has to arrive somewhere the model doesn't treat as
  the client talking (its own thinking? a system message it isn't told to
  use?), or not as language at all.
- Six nudges buy variety, not depth. Depth came once, from re-reading.
- Briefing the client's wants and the scorecard pulled the model toward
  satisfying the scorecard with novelty. Worth remembering for the
  presentation: the eight axes are for judging an answer, and handing them
  to the answerer is a different thing.
- Still untested, now better specified: the practice-move lever. 30/30
  know § 7028.15(e); 0/30 ask the client; 18/30 reach "conditional award"
  but as a cure the bidder is offered, not a condition on execution.

## Handoff (2026-10-28 morning, g5 done) — state for a fresh session

- **g5 batch finished** 00:50 on 2026-10-28: 30 runs
  `runs/g5-{bare,briefed}-{none,placebo,words}-r{1..5}` (qwen3.5:35b) with
  `judge-blind.{json,md}` and `judge-keyed.{json,md}` (qwen3.5:122b) in
  each. Results written up in the g5 results section above.
  `python3 scripts/summarize-g5.py --missing` reproduces the tables.
- Read for yourself: `runs/g5-bare-none-r5/transcript.md` turn 6 (the
  re-read that worked), `runs/g5-briefed-words-r5/transcript.md` turn 1
  (the "Lantern Partnership"), `runs/g5-bare-words-r1/transcript.md` any
  turn (quotes as section headers), `runs/g5-bare-placebo-r2/transcript.md`
  turn 6 ("we do not need a hearing (Rest)"). Thinking is in `<details>`.
- Open: where noise could enter without being read as instruction; the
  practice-move vs doctrine lever (see g4 and the g5 "what this says").
- Earlier handoff follows.

## Handoff (2026-10-27, after g4) — state for a fresh session

- **Repo layout:** `daydream.py` (harness; `--help` is complete), `seeds/`
  (`solar-surplus.md`; `kestrel-r2.md` = the plain Kestrel seed now in use;
  `kestrel-r2-dream.md` = deprecated novel frame), `words/concrete.txt`,
  `runs/g1..g4*`, this file. Source for Kestrel:
  `~/Projects/bid-protest-presentation` (`docs/practice-rules.md`
  I23/I34/I37/I41 for the known novel solutions).
- **Base models now local** (pulled from HF GGUF; names as `ollama list`
  prints them): `hf.co/mradermacher/Qwen3.5-9B-Base-GGUF:q4_K_M`,
  `hf.co/mradermacher/Qwen3.5-35B-A3B-Base-GGUF:q4_K_M`,
  `hf.co/allenai/OLMo-2-1124-7B-GGUF:q4_K_M` (ctx 4096),
  `hf.co/mradermacher/Mistral-7B-v0.3-i1-GGUF:q4_K_M`,
  `hf.co/mradermacher/OLMo-2-0325-32B-GGUF:q4_K_M` (ctx 4096). Use
  `--mode raw` only. Qwen3.5-Base takes default sampling; the 2024-era
  bases need `--temperature 0.6 --min-p 0.05 --repeat-penalty 1.15` and
  **no tag** (the tag is markup to them: `--open-marker= --continue-marker=
  --stop`). Pass `--num-ctx 4096` for OLMo.
- **g4 findings in one line each:** Qwen3.5-Base already contains the
  assistant (hallucinated prompts, `<think>`, markdown). The 35B base's one
  great run (fragment register, verify-before-award) did not replicate 0/3;
  each run picks a different register; a real move ~half the time. OLMo-2
  32B, the only truly self-free model, produces dream affect and no law.
  Noise never surfaced in any base model.
- **Still parked by Nick's choice:** the discriminator pass. The five 35B
  base runs (`g4-base-qwen35b-raw-none*`) are a ready test set if that
  gets unparked.
- **Untested:** practice-move knowledge vs. doctrine (give the model the
  menu of practitioner moves and see whether daydreaming picks among them
  differently than deliberation does); a mid-size clean base between 7B
  and 32B; longer OLMo-32B runs at lower temperature.
- **Known breakage:** mistral-medium-3.5:128b garbage with the novelist
  prompt (frame dropped, not chased). gpt-oss needs `--max-tokens` ≥ 900
  in chat mode.
