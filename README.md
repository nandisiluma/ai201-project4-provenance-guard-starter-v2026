# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

1. Arrive: JSON {text, creator_id} hits /submit. Extract text and creator_id from the payload. Decide here what happens when the text is missing, empty or huge.
2. Assign an ID: a content_id is generated, because /appeal needs it later.
3. Signal one: detector.model_signal(text) gives model_score.
4. Signal two: stylometry.style_signal(text) gives style_score.
5. Combine: scoring.combine_signals(...) turns the two scores into one confidence.
6. Label: scoring.score_to_label(...) maps the score to the label a reader sees.
7. Log and respond: audit.log_decision(...) records both signal scores and the combined one, and the response returns the label.

---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:**
Measures the model signal which is a 0–1 score measure of perplexity. A score of 1 means the text is most likely an AI generated text. A text with a score of 0.5 is a coin flip.

**Why that might differ between human and AI writing:**

Human writing tends to be unpredictable and thus might have a lower perplexity score whereas AI writing tends to be plain, simple and predictable leading to a higher perplexity score.

**What it can't see:**

Authorship. The model signal measures how predictable the text is to gpt2, not who wrote it. It scores common words in short, ordinary sentences as machine-like, and plenty of real people write that way. That includes people writing in a second language who stick to vocabulary they're sure of, younger writers, and anyone who writes plainly on purpose. Plain human writing can score as machine-like as AI output does.

The error also runs the other way. Dense, ornate prose full of rare words can score as human, because a language model is bad at predicting rare words. Being formal doesn't decide the score either way.

### Signal two — the style signal

**What it measures:**

Measures the style signal, the shape of the text, without understanding meaning.

**Why that might differ between human and AI writing:**
Generated prose tends toward even, mid-length sentences and a narrower band of vocabulary, because that's what "most likely next word" produces on average. Human writing is lumpier — a three-word sentence next to a forty-word one.

**What it can't see:**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation.

### Endpoints

**/appeal**
A writer says you got it wrong. ← TODO — Milestone 5

Expects JSON:
{"content_id": "...", "reasoning": "..."}
Returns a confirmed label

**/submit**
Expects JSON:
{"text": "...", "creator_id": "..."}
Returns:
{"content_id": "...", "guess": "...", "confidence": 0.0, "label": "...",
"model_score": 0.0, "style_score": 0.0}

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:**

Average the two scores with equal weight. A text can only reach the high-confidence AI range if both signals independently score it at or above a gate; if either signal is below the gate, the combined score is capped just under the AI threshold, so the most the text can get is "unsure". The human end is not gated. I chose this because accusing a real writer costs that person far more than missing some AI text, and because both of my signals can misread plain human writing, so requiring them to agree before accusing means a single misreading signal can't produce an accusation. The cost is that AI text is accused less often.

**The numbers:**

- Weights: model signal 0.5, style signal 0.5 (`WEIGHT_MODEL_SIGNAL`, `WEIGHT_STYLE_SIGNAL`).
- Agreement gate: 0.7 (`AGREEMENT_GATE`). A guess, to be checked against my calibration inputs.
- Thresholds: human below 0.35, AI above 0.65 (`HUMAN_THRESHOLD`, `AI_THRESHOLD`). The cap is `AI_THRESHOLD - 0.01`.

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**

A lightly edited AI paragraph about social media ("Social media has changed how people talk. It lets friends stay in touch, but it can also make people feel left out. Some people post a lot. Others just scroll and never post at all, which is fine too I guess.") scored model 0.70 and style 0.47. The model signal reads it as AI, but the mix of short and long sentences makes the style signal read it as human-like. The average is about 0.59 and the style score is under the gate, so the rule keeps it at "unsure" instead of picking a side, which is what two signals disagreeing should mean.

Lightly edited AI text:

Social media has changed how people talk. It lets friends stay in touch, but it can also make people feel left out. Some people post a lot. Others just scroll and never post at all, which is fine too I guess.

## Test texts

Four deliberately chosen inputs, each sent through `POST /submit`. Scores are
model / style / combined.

**Clearly human** — 0.31 / 0.26 / 0.29 → `human`

> Okay so — the dog ate my sandwich. Not a metaphor. Actual sandwich, actual dog (Biscuit, a menace). I turned around for ten seconds to answer the door and when I came back there was just a crust and a very guilty face. Dinner was cereal. Again.

**Clearly AI** — 0.86 / 0.70 / 0.78 → `ai`

> Technology plays an important role in modern education. It helps students learn new skills and access useful information. It also helps teachers share lessons and track student progress. Technology makes learning more engaging and more accessible for everyone. It is important for schools to use technology in a thoughtful way. This helps students prepare for the future and succeed in their careers.

**Formal human** — 0.66 / 0.50 / 0.58 → `unsure`

> The committee convened on Tuesday to consider the proposed amendments to the municipal zoning ordinance. After extended deliberation, it was resolved that the residential density limits would remain unchanged, pending a further review of infrastructure capacity. Several members expressed reservations regarding the projected burden on existing water and sewage services; these concerns will be addressed in the subsequent report, which is expected before the close of the fiscal year.

**Lightly-edited AI** — 0.67 / 0.47 / 0.57 → `unsure`

> Remote work has changed how many people think about their jobs. It offers flexibility and saves commuting time, but it can also blur the line between work and home. Some people love it. Others miss the office more than they expected, honestly. Companies are still working out what a good balance looks like, and I suspect they will be for a while yet.

**What surprised me.** A more formal AI paragraph ("Effective communication is a
cornerstone of successful teamwork...") scored model 0.82 but style only 0.54,
and ended at 0.64 — "unsure", not `ai`. Printing the two signals separately
showed the style signal was the one that was off: its vocabulary measure reads
varied, formal wording as human, and the agreement gate (0.7) then stopped the
model signal from accusing on its own. The clearly-AI text above reaches `ai`
only because it uses short, even sentences, repeated words and plain
punctuation, and that is also how a plain human writer can sound. A short plain
human paragraph ("I like my dog. He is brown and he is big...") scored model
0.85 and style 0.69, just under the gate, so it stays at "unsure" only
narrowly.

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label                 | Score range | The exact text a reader sees                                                                                                                                                                       |
| --------------------- | ----------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| high-confidence human | 0.00 – 0.35 | "We think this was probably written by a person."                                                                                                                                                  |
| unsure                | 0.35 – 0.65 | "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it." |
| high-confidence AI    | 0.65 – 1.00 | "This looks like it may have been written by AI. We can get this wrong. If you wrote it yourself, you can appeal and ask for a person to look at it."                                              |

**Why I worded the "unsure" one this way:**

<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->

We're not accusing them outright and also letting them know that they can appeal.

---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "I like my dog. He is brown and he is big. We walk every day after school. He likes the park. I give him food and water. He sleeps on my bed. He is my best friend.", "creator_id": "sample_writer"}'
```

```json
{
  "confidence": 0.64,
  "content_id": "565a35cc-fa71-4381-b0ab-8af41bb98d54",
  "guess": "unsure",
  "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
  "model_score": 0.8537,
  "style_score": 0.6866
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "565a35cc-fa71-4381-b0ab-8af41bb98d54", "reasoning": "I wrote this myself for a class assignment. I write in short, simple sentences."}'
```

```json
{
  "content_id": "565a35cc-fa71-4381-b0ab-8af41bb98d54",
  "message": "Your appeal has been recorded and this submission is now under review.",
  "status": "under_review"
}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json
{
  "count": 3,
  "entries": [
    {
      "combined_score": 0.64,
      "content_id": "838980cd-4274-486a-903d-df8cbf41067d",
      "creator_id": "clearly_ai",
      "guess": "unsure",
      "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
      "model_score": 0.8239,
      "status": "decided",
      "style_score": 0.5411,
      "timestamp": "2026-11-09T04:59:13+00:00"
    },
    {
      "combined_score": 0.64,
      "content_id": "565a35cc-fa71-4381-b0ab-8af41bb98d54",
      "creator_id": "sample_writer",
      "guess": "unsure",
      "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
      "model_score": 0.8537,
      "status": "decided",
      "style_score": 0.6866,
      "timestamp": "2026-11-09T05:05:10+00:00"
    },
    {
      "content_id": "565a35cc-fa71-4381-b0ab-8af41bb98d54",
      "creator_id": "sample_writer",
      "event": "appeal",
      "reasoning": "I wrote this myself for a class assignment. I write in short, simple sentences.",
      "status": "under_review",
      "timestamp": "2026-11-09T05:05:10+00:00"
    }
  ]
}
```

---

## How I Used AI

**Moment 1 — Analyzing the requirements (acceptance criteria)**

- _What I asked for:_ A review of all five of my acceptance criteria for
  testability, after I had written them. Earlier I had also asked what "label
  coverage" means, and how to write a bad-input criterion that doesn't
  contradict my criterion that every test input gets a label.
- _What came back:_ It found that four of my criteria couldn't be checked as
  written. "Recognizes human writing 5/5 times" didn't say whether "unsure"
  counts as a pass. "The spread" didn't say what was being measured or 4/5 of
  what. The label-coverage criterion could never fail, because `score_to_label`
  always returns one of three labels. "A clear message" for bad input was a
  judgment call. For my bad-input worry, it suggested scoping the label
  criterion to valid input only.
- _What I changed:_ I accepted the revised wording for criteria 1, 2, 3 and 5
  and kept the one it said was already fine (the appeal criterion). Each one now
  names a number and a way to check it. I also kept the reasoning in the "why"
  lines as my own: a false accusation costs the writer more than a missed
  detection.

**Moment 2 — Writing and debugging the code**

- _What I asked for:_ Reviews of my own implementations of
  `sentence_length_spread`, `type_token_ratio` and `style_signal`, then help
  building `punctuation_density`, the `/submit` wiring, `score_to_label` and
  `/appeal`. I also asked how a route reads the request when `submit()` takes no
  arguments.
- _What came back:_ Specific bugs I had missed. `l.len()` doesn't exist in
  Python. `for wrd in total_words` loops over an integer. `sum(a, b, c)` takes a
  list, not three arguments. A one-sentence text crashed `stdev`. My first
  "skip the spread" condition (`spread_ai == 1.0`) would also have skipped texts
  whose sentences are all the same length, which is strong AI evidence. It
  explained that `request` is a global Flask object, so `submit()` doesn't
  need a payload argument.
- _What I changed:_ I fixed my own functions from the reviews, and changed the
  skip condition to `len(sentences(text)) < 2`. I disagreed with it once: it
  dropped `?` and `!` from the punctuation count because they end sentences, and
  I pointed out I count the whole text, not sentences. It agreed the reason was
  weaker than it sounded, and I put them back. I ran each change myself with
  `curl` and by reading `/log` instead of trusting that it worked.

**Moment 3 — Developing test scenarios**

- _What I asked for:_ Four test texts: clearly AI, clearly human, formal human
  and lightly-edited AI. Later I asked for texts that would trigger the `human`
  and `ai` labels, since all four of mine came back "unsure".
- _What came back:_ Candidate texts with real scores from my two signals, not
  guesses. The scores showed something I hadn't expected: a plainly written
  human paragraph scored as AI-like on both signals (model 0.85, style 0.69),
  and my style signal scored it higher than a clearly AI paragraph (0.54). It
  searched a batch of candidates and found texts that reach `ai` and `human`,
  and it spotted that my "Human" and "AI" test texts in this README had been
  swapped (both were AI-written).
- _What I changed:_ I used the texts that reach each label as my Test texts and
  fixed the swapped entries. I also proposed giving the style signal more
  weight than the model signal, because I thought plain writing is common among
  humans. The AI tested that against my data and showed it wouldn't help,
  because both signals misread plain writing. I switched to the agreement-gate
  rule in "The combining rule" and recorded the trade-off: fewer false
  accusations, and less AI text caught.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 5 per minute, 50 per day

**Why those numbers and not others:**

The limit counts requests to `POST /submit`, not words: a one-word text and a
5000-character essay each use one request. A real writer pastes in a piece,
waits for the answer, reads it, and maybe revises and tries again, so a few
requests an hour is typical and one every 30 seconds is already fast. Ten a
minute is more than a person needs. Five a minute still
leaves room for a retry after a typo, and 50 a day is well above how many pieces
a writer would check in one sitting. A script mapping my thresholds with
hundreds of variations hits the minute limit after five requests and has to
slow to a crawl. Each request also runs a language model on my laptop, so a
tighter limit protects the service too.

**What a caller counts as:** the `creator_id` in the request body, and the
caller's IP address when there isn't one (`app.py::rate_limit_key`). Per
creator is fairer to a household or classroom sharing one address. The weakness
is that the caller chooses their own `creator_id`, so a script that sends a new
one on every request gets a fresh count each time and is never limited. Limiting
by address would block that, but would treat many people behind one address as
one caller. I kept per creator and know it doesn't stop that attack.

**The run of status codes when I pushed past it:**

```
$ python run_attacks.py --flood 15
15 submissions as 'flood_tester' against http://127.0.0.1:5000

  [ 1/15] 200
  [ 2/15] 200
  [ 3/15] 200
  [ 4/15] 200
  [ 5/15] 200
  [ 6/15] 429
  [ 7/15] 429
  [ 8/15] 429
  [ 9/15] 429
  [10/15] 429
  [11/15] 429
  [12/15] 429
  [13/15] 429
  [14/15] 429
  [15/15] 429

200 200 200 200 200 429 429 429 429 429 429 429 429 429 429
10 of 15 were rate limited.
```

Rejected requests still leave a trace in the log:

```json
{
  "creator_id": "flood_tester",
  "event": "rejected",
  "limit": "5 per 1 minute",
  "reason": "rate_limited",
  "status": "rejected",
  "timestamp": "2026-11-09T18:31:30+00:00"
}
```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->

**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

### EV01 — `evasion`

_Targeting:_ signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "2d9b29b0-83a2-409d-85bd-9f4535c4ddf9",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.3863,
  "model_score": 0.1635,
  "style_score": 0.6092,
  "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
  "error": null,
  "verdict": "HELD"
}
```

### EV04 — `evasion`

_Targeting:_ signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "739c116c-6ae3-4df6-b015-11237328a953",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.6081,
  "model_score": 0.6114,
  "style_score": 0.6048,
  "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
  "error": null,
  "verdict": "HELD"
}
```

### EV05 — `evasion`

_Targeting:_ both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "f9915389-99f9-4873-9d63-ef4b0527e61a",
  "creator_id": "attacker_EV05",
  "guess": "unsure",
  "confidence": 0.3793,
  "model_score": 0.3212,
  "style_score": 0.4375,
  "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
  "error": null,
  "verdict": "HELD"
}
```

### EV07 — `evasion`

_Targeting:_ signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "5bbdf899-4319-4245-b798-06b87b0c1b78",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.3833,
  "model_score": 0.5862,
  "style_score": 0.1804,
  "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
  "error": null,
  "verdict": "HELD"
}
```

### FP02 — `false_positive`

_Targeting:_ human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "22285ab0-6757-40ff-b6be-6f538b50b657",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.64,
  "model_score": 0.7387,
  "style_score": 0.6655,
  "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
  "error": null,
  "verdict": "HELD"
}
```

### FP03 — `false_positive`

_Targeting:_ a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "6c1d634a-c0e0-41b5-a5e2-d6b58f01af7f",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.64,
  "model_score": 0.8051,
  "style_score": 0.6496,
  "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
  "error": null,
  "verdict": "HELD"
}
```

### FP05 — `false_positive`

_Targeting:_ technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "11b56674-1120-4250-8c82-1f26301a9dfa",
  "creator_id": "attacker_FP05",
  "guess": "unsure",
  "confidence": 0.64,
  "model_score": 0.8005,
  "style_score": 0.6744,
  "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
  "error": null,
  "verdict": "HELD"
}
```

### FP08 — `false_positive`

_Targeting:_ very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "dc47971b-6440-42cd-a180-c7901666712e",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.4223,
  "model_score": 0.3223,
  "style_score": 0.5223,
  "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
  "error": null,
  "verdict": "HELD"
}
```

### PI02 — `prompt_injection`

_Targeting:_ instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "a4db3980-7f1c-47eb-894b-e78ae2455cc4",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.3046,
  "model_score": 0.2044,
  "style_score": 0.4049,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_12 — `flood_same_creator`

_Targeting:_ 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

### FP03 — `false_positive`

_Targeting:_ a non-native English speaker writing carefully

The writer is a non-native English speaker who wrote carefully, and the system told them it couldn't tell whether a person wrote it. Signal one scored 0.81 and signal two 0.65, both on the AI side. The only reason this wasn't an "ai" label is the combining rule, which capped it at unsure (0.64). A slightly lower threshold would have accused them outright. Careful, simple prose is low-perplexity, so signal one reads it as AI-written.

---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion          | Target | Run 1  | Run 2  | Run 3  | Verdict |
| ------------------ | ------ | ------ | ------ | ------ | ------- |
| 1. False positives | 3/3    | MET    | MET    | MET    | MET     |
| 2. score spread    | 3/3    | MET    | MET    | MET    | MET     |
| 3. label coverage  | 3/3    | MET    | MET    | MET    | MET     |
| 4. appeal path     | 3/3    | MET    | MET    | MET    | MET     |
| 5. bad input       | 3/3    | MISSED | MISSED | MISSED | MISSED  |

**Real output from trial 1 of `results/run_2026-11-09_1550_before.md`**, pasted as text, one block per criterion. Each block was produced by `run_eval.py::main`, which sends the request and records the response; the service behind it is named in each heading.

#### Criterion 1 — False positives

Produced by `run_eval.py::main` calling `app.py::submit`.

```json
[
  {
    "status": 200,
    "error": null,
    "appeal": null,
    "guess": "unsure",
    "confidence": 0.64,
    "model_score": 0.7193,
    "style_score": 0.5977,
    "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
    "sent": "Good day,Unfortunately due to competing priorities, I will not be able"
  },
  {
    "status": 200,
    "error": null,
    "appeal": null,
    "guess": "unsure",
    "confidence": 0.3662,
    "model_score": 0.3311,
    "style_score": 0.4014,
    "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
    "sent": "Hello, I am reaching out because a Walmart grocery delivery intended f"
  },
  {
    "status": 200,
    "error": null,
    "appeal": null,
    "guess": "unsure",
    "confidence": 0.6072,
    "model_score": 0.7719,
    "style_score": 0.4425,
    "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
    "sent": "Hi Diana, Thank you for following up with me. I realized that I do not"
  },
  {
    "status": 200,
    "error": null,
    "appeal": null,
    "guess": "unsure",
    "confidence": 0.504,
    "model_score": 0.5451,
    "style_score": 0.463,
    "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
    "sent": "Hello CS7 Students, Congratulations again on completing this class! We"
  },
  {
    "status": 200,
    "error": null,
    "appeal": null,
    "guess": "unsure",
    "confidence": 0.5282,
    "model_score": 0.4743,
    "style_score": 0.5821,
    "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
    "sent": "The art of our mindset determines the people we become, directs the wa"
  }
]
```

#### Criterion 2 — score spread

Produced by `run_eval.py::main` calling `app.py::submit`.

```json
[
  {
    "status": 200,
    "error": null,
    "appeal": null,
    "guess": "ai",
    "confidence": 0.781,
    "model_score": 0.8579,
    "style_score": 0.7041,
    "label": "This looks like it may have been written by AI. We can get this wrong. If you wrote it yourself, you can appeal and ask for a person to look at it.",
    "sent": "Technology plays an important role in modern education. It helps stude"
  },
  {
    "status": 200,
    "error": null,
    "appeal": null,
    "guess": "human",
    "confidence": 0.2854,
    "model_score": 0.3099,
    "style_score": 0.2609,
    "label": "We think this was probably written by a person.",
    "sent": "Okay so \u2014 the dog ate my sandwich. Not a metaphor. Actual sandwich, ac"
  },
  {
    "status": 200,
    "error": null,
    "appeal": null,
    "guess": "unsure",
    "confidence": 0.5693,
    "model_score": 0.6698,
    "style_score": 0.4688,
    "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
    "sent": "Remote work has changed how many people think about their jobs. It off"
  }
]
```

#### Criterion 3 — label coverage

Produced by `run_eval.py::main` calling `app.py::submit`.

```json
[
  {
    "status": 200,
    "error": null,
    "appeal": null,
    "guess": "ai",
    "confidence": 0.781,
    "model_score": 0.8579,
    "style_score": 0.7041,
    "label": "This looks like it may have been written by AI. We can get this wrong. If you wrote it yourself, you can appeal and ask for a person to look at it.",
    "sent": "Technology plays an important role in modern education. It helps stude"
  },
  {
    "status": 200,
    "error": null,
    "appeal": null,
    "guess": "human",
    "confidence": 0.2854,
    "model_score": 0.3099,
    "style_score": 0.2609,
    "label": "We think this was probably written by a person.",
    "sent": "Okay so \u2014 the dog ate my sandwich. Not a metaphor. Actual sandwich, ac"
  },
  {
    "status": 200,
    "error": null,
    "appeal": null,
    "guess": "unsure",
    "confidence": 0.5693,
    "model_score": 0.6698,
    "style_score": 0.4688,
    "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
    "sent": "Remote work has changed how many people think about their jobs. It off"
  }
]
```

#### Criterion 4 — appeal path

Produced by `run_eval.py::main` calling `app.py::submit then app.py::appeal`.

```json
[
  {
    "status": 200,
    "error": null,
    "appeal": {
      "status": 200,
      "body_status": "under_review",
      "error": null
    },
    "guess": "unsure",
    "confidence": 0.4306,
    "model_score": 0.461,
    "style_score": 0.4002,
    "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
    "sent": "Good day, due to competing priorities I will not be able to volunteer "
  },
  {
    "status": 200,
    "error": null,
    "appeal": {
      "status": 200,
      "body_status": "under_review",
      "error": null
    },
    "guess": "unsure",
    "confidence": 0.5162,
    "model_score": 0.6372,
    "style_score": 0.3952,
    "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
    "sent": "Hi Diana, thank you for following up. I do not meet the GPA requiremen"
  },
  {
    "status": 200,
    "error": null,
    "appeal": {
      "status": 200,
      "body_status": "under_review",
      "error": null
    },
    "guess": "unsure",
    "confidence": 0.3715,
    "model_score": 0.3451,
    "style_score": 0.3978,
    "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
    "sent": "Okay so, the dog ate my sandwich. Not a metaphor. I turned around for "
  },
  {
    "status": 200,
    "error": null,
    "appeal": {
      "status": 200,
      "body_status": "under_review",
      "error": null
    },
    "guess": "unsure",
    "confidence": 0.64,
    "model_score": 0.7691,
    "style_score": 0.5834,
    "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
    "sent": "Remote work has changed how many people think about their jobs. It off"
  },
  {
    "status": 200,
    "error": null,
    "appeal": {
      "status": 200,
      "body_status": "under_review",
      "error": null
    },
    "guess": "unsure",
    "confidence": 0.64,
    "model_score": 0.8341,
    "style_score": 0.6143,
    "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
    "sent": "Technology plays an important role in modern education. It helps stude"
  },
  {
    "sent": "(unknown content_id)",
    "appeal": {
      "status": 404,
      "body_status": null,
      "error": "unknown_content_id"
    }
  }
]
```

#### Criterion 5 — bad input

Produced by `run_eval.py::main` calling `app.py::submit`.

```json
[
  {
    "status": null,
    "error": "JSONDecodeError: Expecting value: line 1 column 1 (char 0)",
    "sent": "{\"creator_id\": \"eval_bad_missing\"}"
  },
  {
    "status": null,
    "error": "JSONDecodeError: Expecting value: line 1 column 1 (char 0)",
    "sent": "{\"text\": null, \"creator_id\": \"eval_bad_null\"}"
  },
  {
    "status": null,
    "error": "JSONDecodeError: Expecting value: line 1 column 1 (char 0)",
    "sent": "(empty text)"
  },
  {
    "status": 200,
    "error": null,
    "appeal": null,
    "guess": "unsure",
    "confidence": 0.5,
    "model_score": 0.0,
    "style_score": 1.0,
    "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
    "sent": "   \n\t  "
  },
  {
    "status": 200,
    "error": null,
    "appeal": null,
    "guess": "ai",
    "confidence": 0.9985,
    "model_score": 0.9975,
    "style_score": 0.9995,
    "label": "This looks like it may have been written by AI. We can get this wrong. If you wrote it yourself, you can appeal and ask for a person to look at it.",
    "sent": "word word word word word word word word word word word word word word "
  }
]
```

The first three bodies (missing `text`, `text: null`, empty string) show `status: null` with `JSONDecodeError` because `app.py::submit` has no input validation. It crashes instead of returning a JSON error, so `run_eval.py` could not parse a response. The whitespace-only and 5,500-character bodies both returned `200` with a score and label, so criterion 5 is missed.

**Diagnoses**

Scores below are `model_score` / `style_score` from `results/attack_run_2026-11-09_1247.md` and `results/run_2026-11-09_1550_before.md`.

#### Criterion 5 (bad input) — missed in 3/3 trials

**Stage: the route (`app.py::submit`).** The route does no validation. It does `payload = request.get_json(silent=True) or {}`, takes `text` and `creator_id` as they are, and passes `text` straight to `detector.model_signal`. Nothing rejects bad input before a signal sees it, so each case fails differently:

- Missing `text`, `text: null` and empty body all reach `text = None`, and the tokenizer raises `ValueError: You need to specify either text or text_target` (RQ01, RQ05, RQ08, RQ09). In the eval these show as `JSONDecodeError` because Flask answered with an HTML 500 page.
- An empty string and a one-character string reach `detector.perplexity`, which raises `ValueError: Text is too short to score` (criterion 5's empty string, MF02). The route never catches it.
- Whitespace-only text is never stripped, so it is scored: `model_score` 0.0, `style_score` 1.0, label `unsure`, 200.
- Text over 5,000 characters has no length cap. The 5,500-character `"word word …"` body scored 0.9975 / 0.9995 and was labelled `ai` at 0.9985, 200.

#### Attacks that crashed the service (9 auto-BROKE)

All nine are the same stage and mechanism as criterion 5: **the route** trusts the payload shape and type.

| Attacks                | Mechanism                                                                                                                                                           |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| RQ01, RQ05, RQ08, RQ09 | `text` is `None` (missing key, null, unparseable body, empty body). `get_json(silent=True)` swallows the parse error and the tokenizer raises.                      |
| RQ07                   | Body is a JSON array. `payload` is a non-empty list, so `or {}` doesn't replace it and `payload.get` raises `AttributeError: 'list' object has no attribute 'get'`. |
| RQ03, RQ12             | `text` is a number or nested object. Nothing checks `isinstance(text, str)`, and the tokenizer raises `ValueError: text input must be of type str`.                 |
| RQ04, MF02             | `text` is a list or a single character. The tokenizer accepts the list, and `perplexity` raises `Text is too short to score`. The route doesn't catch it.           |

RQ10 and RQ11 were marked HELD, but they came back 429 from the rate limiter, not from validation. The route never ran for them, so they are untested.

#### Bad input that scored 200 and shouldn't have (script said HELD)

These got a label instead of a rejection. The route lets them through, and the signals and combining rule then turn them into a confident answer.

- **MF06 (emoji only, `ai` 0.9985) and MF07 (Arabic, `ai` 0.9532): signal two, then the combining rule.** `stylometry.words()` matches only `[a-z0-9']+`, so these texts have zero words. `type_token_ratio` and `punctuation_density` return 0.0 for "no words", which `style_signal` flips to maximum AI, so `style_score` is 1.0. Signal one (0.9969 and 0.9064) also scores them as predictable. Both signals clear `AGREEMENT_GATE` (0.7), so the gate passes them as agreement.
- **MF08 (60,000 characters of ordinary diary writing, `ai` 0.9084): signal two.** `style_score` is 0.8292 because `type_token_ratio` falls as text gets longer, which the function's own docstring warns about. Signal one only reads the first 400 tokens (`DETECTOR_MAX_TOKENS`) and gave 0.9876. The route has no length cap.
- **MF05 (one very long word, 0.64) and MF01/MF04 (whitespace and punctuation only):** the same zero-word defaults in signal two. MF05 only stays `unsure` because its `style_score` is 0.5, under the gate.

#### Evasion attacks that got AI text under the `ai` line (EV01–EV09)

The attack script marked all nine HELD because the service answered 200. But only EV10 was labelled `ai`. EV10 repeats a stanza, which is the one case where cheap structure helps the detector. The other nine were all pushed into `unsure`, so the evasions somewhat worked.

**Pattern, and the stage: the combining rule (`scoring.py::combine_signals`).** It only allows `ai` when both signals are at or above 0.7. That was my deliberate protection for human writers, but it means an evader only has to beat one signal. Whichever signal was weakened, the score is capped at 0.64.

| Attack                                      | model / style   | Signal that moved, and why                                                                                                                                                   |
| ------------------------------------------- | --------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| EV01 typos                                  | 0.1635 / 0.6092 | **Signal one.** The typos made rare tokens gpt2 can't predict, so perplexity rose and `model_score` collapsed. I had expected signal two (type-token ratio) to take the hit. |
| EV02 broken-up sentences                    | 0.5943 / 0.3983 | **Signal two.** `sentence_length_spread` rose.                                                                                                                               |
| EV03 pasted quotation                       | 0.6662 / 0.4843 | **Signal two.** The quotation changed sentence spread and vocabulary variety.                                                                                                |
| EV04 unusual words                          | 0.6114 / 0.6048 | **Signal one** (rare words raise perplexity). Signal two also dropped to 0.6048.                                                                                             |
| EV05 heavy edit                             | 0.3212 / 0.4375 | Both signals.                                                                                                                                                                |
| EV06 one very long, one very short sentence | 0.5727 / 0.3732 | **Signal two.** The length spread term was maxed out.                                                                                                                        |
| EV07 punctuation padding                    | 0.5862 / 0.1804 | **Signal two.** `punctuation_density` is capped at 0.25 in `style_signal`, so padding zeroes that term.                                                                      |
| EV08 text below the token window            | 0.2452 / 0.5724 | **Signal one.** A very short text has no context for gpt2, so perplexity is high.                                                                                            |
| EV09 human opening bolted on                | 0.7042 / 0.5018 | **Signal two.** It measures the whole text, so the human paragraph dilutes it. Signal one stayed above 0.7.                                                                  |

Signal two is the cheaper one to beat (EV02, EV03, EV06, EV07, EV09). It is also the one that measures shape without reading, which is the blind spot I named in Milestone 1.

#### Held, with a note

- **False positives (FP02–FP07) all scored exactly 0.64.** Signal one scored 0.74–0.88 on careful, plain human writing (FP03: 0.8051). Only the gate stopped these from being `ai`, because signal two stayed under 0.7 (0.56–0.67), and the cap is 0.01 below the threshold. Criterion 1 is met because of the combining rule, not because signal one is accurate. This is the same mechanism as FP03 above.
- **Prompt injection (PI01–PI06) and flooding (FL01) held.** The detector is gpt2 perplexity plus text statistics, so it never follows instructions in the text. The flood was cut off by the rate limiter after 5 requests.

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->

---

## The Improvement

**What I changed:**

I added input validation to the route, `app.py::submit`, and a length limit, `MAX_TEXT_CHARS = 5000`, in `config.py`. Before any signal sees the text, `submit()` now rejects:

| Input                                                          | Status | `error`             |
| -------------------------------------------------------------- | ------ | ------------------- |
| Body isn't a JSON object (array, unparseable, empty)           | 400    | `invalid_body`      |
| `text` missing or null                                         | 400    | `missing_text`      |
| `text` isn't a string (number, list, object)                   | 400    | `text_not_a_string` |
| Empty or whitespace-only `text`                                | 400    | `empty_text`        |
| `text` over 5,000 characters                                   | 413    | `text_too_long`     |
| No English letters or digits (emoji, Arabic, punctuation only) | 422    | `no_readable_text`  |
| Too few tokens for the model to score                          | 422    | `text_too_short`    |

Each rejection goes through `app.py::_reject`, which writes `audit.log_rejection(...)` and returns the 4xx. A bad request is never scored or labelled, and it still leaves an entry in `/log`:

```json
{
  "timestamp": "2026-11-09T22:41:57+00:00",
  "creator_id": "eval_bad_whitespace",
  "event": "rejected",
  "status": "rejected",
  "reason": "empty_text"
}
```

**Which diagnosis pointed at it:**

The criterion 5 diagnosis and the "9 auto-BROKE" diagnosis. Both named the route as the stage: it passed `text` to the signals without checking its type or content. The "bad input that scored 200" diagnosis (MF06 emoji, MF07 Arabic, MF08 at 60,000 characters) pointed at the same place. The signals can't tell that a text is not real text, so the route has to reject it first.

### Attack Run — After

Produced by `run_attacks.py::main`, saved in `results/attack_run_2026-11-09_1641_after.md`. The criteria table is from `run_eval.py::main`, in `results/run_2026-11-09_1641_after.md`.

| Criterion          | Target | Run 1 | Run 2 | Run 3 | Verdict |
| ------------------ | ------ | ----- | ----- | ----- | ------- |
| 1. False positives | 3/3    | MET   | MET   | MET   | MET     |
| 2. score spread    | 3/3    | MET   | MET   | MET   | MET     |
| 3. label coverage  | 3/3    | MET   | MET   | MET   | MET     |
| 4. appeal path     | 3/3    | MET   | MET   | MET   | MET     |
| 5. bad input       | 3/3    | MET   | MET   | MET   | MET     |

|                                        | Before (`attack_run_2026-11-09_1247.md`)                               | After (`attack_run_2026-11-09_1641_after.md`) |
| -------------------------------------- | ---------------------------------------------------------------------- | --------------------------------------------- |
| Attacks that crashed (5xx)             | 9                                                                      | 0                                             |
| Malformed bodies answered with a label | MF06 `ai` 0.9985, MF07 `ai` 0.9532, MF08 `ai` 0.9084, MF01/MF04 scored | none, all rejected 4xx                        |
| Criterion 5                            | MISSED in 3/3 trials                                                   | MET in 3/3 trials                             |

Real output for criterion 5 after the change (`run_eval.py::main`, trial 1, same five bodies as before):

```json
[
  {
    "status": 400,
    "error": "missing_text",
    "guess": null,
    "label": null,
    "sent": "{\"creator_id\": \"eval_bad_missing\"}"
  },
  {
    "status": 400,
    "error": "missing_text",
    "guess": null,
    "label": null,
    "sent": "{\"text\": null, \"creator_id\": \"eval_bad_null\"}"
  },
  {
    "status": 400,
    "error": "empty_text",
    "guess": null,
    "label": null,
    "sent": "(empty text)"
  },
  {
    "status": 400,
    "error": "empty_text",
    "guess": null,
    "label": null,
    "sent": "   \n\t  "
  },
  {
    "status": 413,
    "error": "text_too_long",
    "guess": null,
    "label": null,
    "sent": "word word word word word word word word word word word word word word "
  }
]
```

The other two trials are identical.

**Did it help, and how do I know:**

Yes. All five bad inputs now return a 4xx with an `error` field and no label, in all three trials. The audit log has a matching `rejected` entry for each reason (`missing_text`, `empty_text`, `text_too_long`, `no_readable_text`, `text_not_a_string`, `invalid_body`, `text_too_short`). Criterion 5 went from MISSED to MET, and the 9 crashes are gone. All 9 attacks that crashed before now return a clean 4xx (MF02 422, the rest 400), and the three that got a confident label on non-text (MF06, MF07, MF08) are rejected.

It did not change anything for real text. The false-positive attacks (FP02–FP07) still score exactly 0.64, and the evasions EV01–EV09 still score `unsure`, with the same scores as before the change. Validation fixed the route stage only.

---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->

Input validation closed every crash and every malformed-input case. The attack run now has 0 crashes and criterion 5 is met. What is still open:

**1. Evasions EV01–EV09 still get AI text under the `ai` label (scored `unsure`, 0.38–0.61).**

- **Stage and mechanism:** the combining rule needs both signals at 0.7 or higher to say `ai`, so weakening one signal is enough. Typos and unusual words pull down signal one. Sentence splitting, quotations and punctuation padding pull down signal two.
- **What I'd do:** make signal two harder to move, for example by dropping the capped punctuation term that padding can zero out, and by scoring sentence spread on a median instead of a standard deviation. I'd also normalize typos before signal one runs.
- **Why I stopped:** every fix that makes the score easier to push toward `ai` also pushes FP02–FP07 toward `ai`. I had no time to test that trade, and I won't risk accusing a real writer for it.

**2. Human writing is protected by one number.**

- FP02–FP07 all score exactly 0.64, which is the cap, 0.01 under the `ai` threshold. Signal one gave them 0.74–0.88, so it is wrong about all six. Only the gate stops an accusation.
- **What I'd do:** replace gpt2 perplexity, or add a third signal that doesn't punish plain vocabulary.
- **Why I stopped:** that is a redesign of signal one, not a tuning change.

**3. Non-English text is now rejected, not judged.**

- `no_readable_text` rejects any text with no English letters or digits (MF07, the Arabic sample). That is the right call for a detector that can't score it, but a writer in another language gets an error and no appeal path, because no `content_id` is created.
- **What I'd do:** accept these and return `unsure` with a label saying the check doesn't support this language.
- **Why I stopped:** it needs a decision about what the label should say.

**4. RQ10 and RQ11 are still untested.**

- Both came back 429 from the rate limiter in the after run, so the route never ran for them. I haven't confirmed that a form-encoded body or a wrong content type is rejected cleanly. The code should return `invalid_body`, since `get_json(silent=True)` returns `None`.
- **What I'd do:** re-run them after a minute, or with rate limiting off.

**5. Weak spots in the eval itself.** Criterion 4 appeals each ID once. I haven't tested appealing the same `content_id` twice, which `appeal()` would record twice.

**The trade I'd make if this ran for real:**

I would keep the same logic and accept that some AI text, including every evasion above, gets through as `unsure`, because a false `ai` label costs a real writer their reputation, and a missed detection costs very little. The people who pay for it are the readers and the honest writers on the site, who compete with undisclosed AI text, and I'd accept that cost over accusing one person wrongly.

### Unit 9: after the rate-limit change

The rate-limit run log (above, "Unit 9 run log") met 10 of its 11 criteria in
all three runs and could not fully test the other. Nothing was missed, so what is
left is what the run didn't prove and where the targets were set too low.

**Criterion 2 (score spread) is not really tested.**

- It asks for 5 AI/human pairs and `scenarios.py` sends 3 texts, so 2 pairs. Both
  clear 0.2, but "at least 4 of 5" was never measured, and the Unit 8 table's
  MET for it rested on the same 2 pairs.
- **What I'd do:** write three more pairs, each AI text matched to a human one on
  the same topic, and re-run. **Why I stopped:** I wrote the criteria after the
  fix and ran out of time to collect the writing. The pairs need real human text
  on a topic, and I didn't want to make some up.

**Criterion 11 doesn't cover timeouts.**

- There is no server-side time limit on scoring, so a request that hangs would
  hang. Only the test scripts time out (90 s).
- **What I'd do:** run `detector.model_signal` with a timeout, return a `504` and
  write an `error` record. **Why I stopped:** it is a change to the scoring path
  and I wanted the failure handling that already exists tested first.

**Targets I set too low:**

- **Criterion 1.** "None of 5 labelled `ai`" is met by labelling everything
  `unsure`, and that is what happened: all 5 of my own pieces came out `unsure`,
  none `human`. I'd tighten it to "none `ai`, and at least 2 of 5 labelled
  `human`". It would be missed today (0 of 5), which is the point.
- **Criterion 3.** Label coverage passes whenever each label shows up once, which
  says the ranges have no gap but nothing about whether the labels are right. I'd
  tighten it to the combined-score ranges, for example "the clearly-AI text is
  `ai` and the clearly-human text is `human` in 3 of 3 runs".
- **Criterion 6.** The address cap of 20 a minute is high enough that one
  address gets 20 free scored runs a minute. I'd tighten it to match a real
  household, for example 12 a minute, once I know how many people share an
  address.

**Rate-limit weak spots I haven't fixed:**

- Counts live in memory (`memory://`). Under `gunicorn` with several workers, each
  worker counts separately, so the real limit is roughly the limit times the
  number of workers. The fix is shared storage such as Redis.
- Behind a proxy every user looks like one address, so everyone would share the 20
  a minute. The fix is trusting `X-Forwarded-For`, which needs to be configured
  with care or an attacker can fake it.
- A caller with many addresses still gets a quota per address. Stopping that
  needs accounts, which I said I'm not building.
- `Retry-After` can read 61 on a one-minute window because the reset time is
  rounded up.
- `run_eval.py` and `run_attacks.py` are slowed to about 20 requests a minute by
  the address cap, so the full attack set takes much longer or returns mostly
  `429`.

**What I'd do next.** First I'd write the three missing AI/human pairs and
measure criterion 2 properly, because every other result here rests on the two
signals telling AI from human, and that is the one claim I have measured on only
two pairs. Everything else on this list is hardening around a detector whose main
number I haven't yet earned.

<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->
<!-- ═════════════════════════════════════════════════════════════════════


UNIT 9 : Improving Provernance Guard


═════════════════════════════════════════════════════════════════════ -->

## Instrumentation

Every request to `/submit` leaves one structured record, a JSON object on one
line of the audit log (`logs/audit.jsonl`, written by `audit.py`). It is a file
you can read back with `GET /log` or `audit.read_entries()`, not a `print()`.
Successes and failures share the same trace fields, so a run is never visible
only as an absence.

| Field                                                            | Where                 | What it is                                                                                                                                         |
| ---------------------------------------------------------------- | --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `timestamp`                                                      | all                   | UTC time the record was written                                                                                                                    |
| `input_preview`, `input_chars`                                   | all                   | First 100 characters of the submitted `text`, and its full length (`null` when there was no usable text)                                           |
| `guess`, `label`, `model_score`, `style_score`, `combined_score` | decisions             | The output: what the system decided and the three scores behind it                                                                                 |
| `duration_ms`                                                    | all                   | Wall time of the whole request, from the first line of the request to the log write                                                                |
| `model_ms`, `style_ms`                                           | decisions             | Time in signal one (gpt2) and signal two, so a slow run can be pinned to a stage                                                                   |
| `event`, `status`, `reason`, `http_status`                       | rejections and errors | `rejected` = the service refused the input (400/413/422/429). `error` = the service itself failed (500/503), with `error_type` and `error_message` |
| `scope`, `retry_after`                                           | 429s                  | Which limit tripped and how long to wait                                                                                                           |

Anything the service crashes on is caught by one error handler. It logs an
`error` record and returns `{"error": ..., "evaluated": false}`, where it used
to return a bare 500 and leave nothing behind.

`python measure_cost.py` produced the records below. It writes to
`logs/instrumentation_run.jsonl`, not the real audit log, so it doesn't add to
the attack evidence. The real model ran; the texts are 10 different pieces of
writing.

**Ten successful runs** (`cost_probe_1` to `cost_probe_10`):

```json
{"timestamp": "2026-11-16T21:28:20+00:00", "content_id": "af388215-3747-4445-8c1d-67c6b6ab52d4", "creator_id": "cost_probe_1", "guess": "human", "model_score": 0.3099, "style_score": 0.2609, "combined_score": 0.2854, "label": "We think this was probably written by a person.", "status": "decided", "model_ms": 118.6, "style_ms": 0.2, "duration_ms": 119.4, "input_chars": 244, "input_preview": "Okay so — the dog ate my sandwich. Not a metaphor. Actual sandwich, actual dog (Biscuit, a menace). "}
{"timestamp": "2026-11-16T21:28:20+00:00", "content_id": "4f275d0c-3486-4a98-adbc-aab1cecc4f30", "creator_id": "cost_probe_2", "guess": "ai", "model_score": 0.8579, "style_score": 0.7041, "combined_score": 0.781, "label": "This looks like it may have been written by AI. We can get this wrong. If you wrote it yourself, you can appeal and ask for a person to look at it.", "status": "decided", "model_ms": 135.1, "style_ms": 0.2, "duration_ms": 136.0, "input_chars": 400, "input_preview": "Technology plays an important role in modern education. It helps students learn new skills and acces"}
{"timestamp": "2026-11-16T21:28:21+00:00", "content_id": "65bcbd6d-4df8-4421-af8e-4df6c67ebda3", "creator_id": "cost_probe_3", "guess": "unsure", "model_score": 0.6591, "style_score": 0.5049, "combined_score": 0.582, "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.", "status": "decided", "model_ms": 155.6, "style_ms": 0.3, "duration_ms": 156.6, "input_chars": 485, "input_preview": "The committee convened on Tuesday to consider the proposed amendments to the municipal zoning ordina"}
{"timestamp": "2026-11-16T21:28:21+00:00", "content_id": "d01d5569-bb7a-40e2-8d08-a39e2c90bea5", "creator_id": "cost_probe_4", "guess": "unsure", "model_score": 0.6698, "style_score": 0.4688, "combined_score": 0.5693, "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.", "status": "decided", "model_ms": 143.0, "style_ms": 0.2, "duration_ms": 144.0, "input_chars": 351, "input_preview": "Remote work has changed how many people think about their jobs. It offers flexibility and saves comm"}
{"timestamp": "2026-11-16T21:28:21+00:00", "content_id": "68ae94e7-787a-409c-85f3-191739114a16", "creator_id": "cost_probe_5", "guess": "unsure", "model_score": 0.8668, "style_score": 0.6347, "combined_score": 0.64, "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.", "status": "decided", "model_ms": 96.4, "style_ms": 0.2, "duration_ms": 97.2, "input_chars": 144, "input_preview": "I like my dog. He is brown and he is big. He likes to run in the park. We play with a ball every day"}
{"timestamp": "2026-11-16T21:28:21+00:00", "content_id": "a3241cee-ceb9-450a-9391-de753ced8428", "creator_id": "cost_probe_6", "guess": "unsure", "model_score": 0.7814, "style_score": 0.5737, "combined_score": 0.64, "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.", "status": "decided", "model_ms": 91.1, "style_ms": 0.2, "duration_ms": 92.0, "input_chars": 234, "input_preview": "Effective communication is a cornerstone of successful teamwork. When team members share information"}
{"timestamp": "2026-11-16T21:28:21+00:00", "content_id": "e5993ba7-1534-46f3-b1a7-243692315be9", "creator_id": "cost_probe_7", "guess": "unsure", "model_score": 0.4231, "style_score": 0.3258, "combined_score": 0.3744, "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.", "status": "decided", "model_ms": 101.6, "style_ms": 0.2, "duration_ms": 102.6, "input_chars": 213, "input_preview": "My grandmother kept a tin of buttons she never used, and when she died we found out why: every butto"}
{"timestamp": "2026-11-16T21:28:21+00:00", "content_id": "6fa22604-5f9e-4ac4-8577-29fe574b05c5", "creator_id": "cost_probe_8", "guess": "unsure", "model_score": 0.8112, "style_score": 0.5175, "combined_score": 0.64, "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.", "status": "decided", "model_ms": 166.4, "style_ms": 0.2, "duration_ms": 167.1, "input_chars": 295, "input_preview": "The results indicate a statistically significant improvement in retention among participants who rec"}
{"timestamp": "2026-11-16T21:28:21+00:00", "content_id": "e7966c49-8495-4d83-af44-56a37969c61e", "creator_id": "cost_probe_9", "guess": "unsure", "model_score": 0.3141, "style_score": 0.4486, "combined_score": 0.3813, "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.", "status": "decided", "model_ms": 97.8, "style_ms": 0.2, "duration_ms": 98.6, "input_chars": 216, "input_preview": "Went to the market early, before the heat. Bought peaches, too many, and a loaf that was still warm."}
{"timestamp": "2026-11-16T21:28:21+00:00", "content_id": "9b63194d-87da-4662-aad4-e8c7f64ed37e", "creator_id": "cost_probe_10", "guess": "unsure", "model_score": 0.9511, "style_score": 0.463, "combined_score": 0.64, "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.", "status": "decided", "model_ms": 106.2, "style_ms": 0.2, "duration_ms": 107.1, "input_chars": 306, "input_preview": "Climate change is one of the most pressing challenges of our time. It affects ecosystems, economies,"}
```

**Failed and refused runs**, one per failure path:

```json
{"timestamp": "2026-11-16T21:28:21+00:00", "creator_id": "fail_empty", "event": "rejected", "status": "rejected", "reason": "empty_text", "http_status": 400, "duration_ms": 0.6, "input_chars": 2, "input_preview": "  "}
{"timestamp": "2026-11-16T21:28:21+00:00", "creator_id": "fail_missing", "event": "rejected", "status": "rejected", "reason": "missing_text", "http_status": 400, "duration_ms": 0.5, "input_chars": null, "input_preview": null}
{"timestamp": "2026-11-16T21:28:21+00:00", "creator_id": "fail_long", "event": "rejected", "status": "rejected", "reason": "text_too_long", "http_status": 413, "length": 10000, "duration_ms": 0.5, "input_chars": 10000, "input_preview": "word word word word word word word word word word word word word word word word word word word word "}
{"timestamp": "2026-11-16T21:28:21+00:00", "creator_id": "anonymous", "event": "rejected", "status": "rejected", "reason": "invalid_body", "http_status": 400, "duration_ms": 0.6, "input_chars": null, "input_preview": null}
{"timestamp": "2026-11-16T21:28:21+00:00", "creator_id": "fail_emoji", "event": "rejected", "status": "rejected", "reason": "no_readable_text", "http_status": 422, "duration_ms": 0.8, "input_chars": 7, "input_preview": "🙂🙂🙂 ???"}
{"timestamp": "2026-11-16T21:28:21+00:00", "creator_id": "fail_detector", "event": "error", "status": "error", "reason": "detector_unavailable", "http_status": 503, "error_type": "DetectorUnavailable", "error_message": "model files missing", "path": "/submit", "duration_ms": 0.7, "input_chars": 400, "input_preview": "Technology plays an important role in modern education. It helps students learn new skills and acces"}
{"timestamp": "2026-11-16T21:28:21+00:00", "creator_id": "fail_crash", "event": "error", "status": "error", "reason": "internal_error", "http_status": 500, "error_type": "RuntimeError", "error_message": "simulated crash in signal one", "path": "/submit", "duration_ms": 0.4, "input_chars": 400, "input_preview": "Technology plays an important role in modern education. It helps students learn new skills and acces"}
{"timestamp": "2026-11-16T21:28:22+00:00", "creator_id": "fail_flood", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "5 per 1 minute", "scope": "creator", "retry_after": 60, "duration_ms": 0.5, "input_chars": 144, "input_preview": "I like my dog. He is brown and he is big. He likes to run in the park. We play with a ball every day"}
```

How these were produced, so they aren't misread: the first five are inputs the
service correctly refused (empty text, missing text, 10,000 characters, a body
that is a list not an object, text with no English words). The `429` is the
sixth request from one `creator_id` in a minute. The two `error` records,
`detector_unavailable` (503) and `internal_error` (500), were **induced**: the
script made `detector.model_signal` raise on purpose. I haven't seen the
detector fail unprompted. The point is that when it does, it leaves a record.

---

## What It Costs

The real cost of this system is compute on my own machine. Nothing is called
over the network, so API spend is $0 and no tokens are billed. The unit I
measured is seconds per `/submit` run.

**Result: about 0.12 s of wall time and 0.46 s of CPU time per run, averaged
over 10 runs.** The first request after a start costs about 8 s extra, because
it loads the model.

|                   | Mean        | Min     | Max     |
| ----------------- | ----------- | ------- | ------- |
| Wall time per run | **0.123 s** | 0.093 s | 0.168 s |
| CPU time per run  | **0.455 s** | 0.365 s | 0.616 s |

**How I measured it** (`python measure_cost.py`, output in `results/cost_run.md`):

1. Start the real `gpt2` model on CPU (a Mac, Python 3.12, no GPU).
2. Send one request and time it on its own. That is the cold start: 8.13 s wall,
   6.72 s CPU. It is not in the average, because a running service pays it once.
3. Send 10 different texts (144 to 485 characters, mean 289), one request each,
   through Flask's test client in the same process, so there is no network time.
4. For each run, wall time is `time.perf_counter()` around the request, and CPU
   time is `time.process_time()` over the same span. Average the 10.

CPU time is higher than wall time because torch runs on several threads at once,
so the process burns more CPU-seconds than the clock shows. If this ran on a
paid host billed by CPU-seconds, 0.455 is the number to use, and 0.123 is what a
person waits.

Caveats: the average depends on text length (the longest, 485 characters, took
0.158 s and the shortest, 144 characters, 0.098 s), the texts are short, a single
run on one machine isn't a benchmark, and a request that is refused before
scoring costs under a millisecond (`duration_ms` is 0.4 to 0.8 in the failed
entries above), so a flood of bad requests is cheap for the service to turn away
and a flood of valid ones is not.

**What it would cost for a hundred people a day.** The unit is CPU-seconds, so
this is multiplication, using the measured 0.455 CPU-s and 0.123 s wall per run.
The count of runs is my assumption: a writer checks a few pieces in a sitting,
so I take 5 submissions each. The limit allows 50 a day, so that is the ceiling.

```
Typical:  100 people x 5 submissions/day  = 500 runs/day
          500 runs x 0.455 CPU-s          = 227.5 CPU-s  = 3.8 CPU-minutes/day
          500 runs x 0.123 s wall         =  61.5 s of waiting, all day
          227.5 CPU-s / 86,400 s in a day = 0.26% of one core

Ceiling:  100 people x 50 submissions/day = 5,000 runs/day
          5,000 runs x 0.455 CPU-s        = 2,275 CPU-s = 37.9 CPU-minutes/day
          2,275 CPU-s / 86,400 s          = 2.6% of one core
```

For a hundred people a day this costs about 4 CPU-minutes of one core (38 at the
per-writer limit), $0 in API spend, so the compute is almost nothing and the real
cost is keeping a server with enough memory for `torch` and `gpt2` up all day,
because `RUNNING.md` shows that doesn't fit a free 512 MB host.

---

## The Shape

**What the project is.** Provenance Guard is a small Flask web service that
guesses whether a piece of writing was produced by a person or by an AI, and
says so in a label a reader can see. A writer or a platform sends
`POST /submit` with `{text, creator_id}`. The service scores the text with two
signals that measure different things:

- **Signal one**, `detector.py`: how predictable the text is to a local gpt2
  model (perplexity).
- **Signal two**, `stylometry.py`: the shape of the text, such as sentence-length
  spread, vocabulary range and punctuation, without reading for meaning.

`scoring.py` combines them into one confidence. An `ai` result needs both signals
at 0.7 or higher, so one misreading signal can't accuse a human writer alone.
The label (`ai`, `human` or `unsure`), both signal scores and a `content_id` come
back in the response and go into the append-only audit log (`audit.py`). A writer
who disagrees can `POST /appeal` with that `content_id`, which records the appeal
beside the original decision and moves it to `under_review`. Requests are
validated before any signal sees them, and `/submit` is rate limited. The design
rests on one trade: a wrong accusation of a real writer costs far more than a
missed AI text, so the system prefers `unsure` to a wrong `ai`.

**What we're changing.** The focus area is rate limiting.
Today the limit is keyed on the `creator_id` the caller sends, so a script that
rotates it gets a fresh quota every request and is never limited. The change is to firstly, close that bypass without
punishing real writers who share an address, then show before and after results.
Secondly, a 429 used to say only "Try again
shortly," so a script had no way to know how long to wait and would retry at
once and stay blocked. Now the 429 tells the caller how to recover:

- A `Retry-After` header with the seconds until the window that tripped resets.
- A JSON body with `retry_after` (the same number), `scope` (`address` for the
  shared per-address cap, `creator` for the per-writer cap) and
  `"evaluated": false`. That last field means the text was not classified. A
  rejection is not a `human` verdict and carries no `label`, so a caller can't
  mistake "not checked" for "fine."
- An audit entry for the rejection that also records `scope` and `retry_after`,
  so a burst of rejections shows up as a pattern in the log.

`test_rate_limit.py` checks the header, the body fields, the address scope and
the audit entry. `run_attacks.py` and `run_eval.py` do not yet wait out
`Retry-After` and retry, so they still count a 429 as a plain rejection.

**Scope of the evidence.** For this change, rate limiting is checked with
`run_attacks.py --flood N` (`run_flood`) only, plus `test_rate_limit.py`. The
before and after flood runs are the evidence.

**What's out of scope.** Four things I considered and am not doing:

- **I'm not touching the detection signals or the combining rule.** The weak
  spots in "What's Still Broken" (the evasions EV01–EV09, and signal one scoring
  plain human writing at 0.74–0.88) are real, but fixing them means redesigning
  signal one or adding a third signal, and that risks pushing FP02–FP07 toward
  `ai`. The detection code is untouched: the diff is only
  the limiter decorators, the 429 handler and config, so scores and labels do not change.
- **I'm not using the full attack run or the eval run to judge this change.**
  `run_attacks.py --set …` and `run_eval.py` send many `creator_id`s from one
  address, so under the new address cap they mostly return 429. Only the flood
  attack is meant to exercise rate limiting, so their before and after scores
  are not compared.
- **I'm not adding accounts or authentication.** The only way to fully stop one
  person from using many `creator_id`s is to make a `creator_id` something the
  caller can't invent, such as a login or an API key. That is a different system
  with its own storage, signup and abuse problems. I'm limiting by what the
  server can see, the caller's address, and I accept that an attacker with many
  addresses still gets a quota per address.
- **I'm not changing the storage or deployment.** Counts stay in memory
  (`memory://`), so a restart still clears them. Moving them to Redis, or
  putting the service behind a proxy and trusting `X-Forwarded-For`, is a
  deployment change. It is a separate piece of work from closing the
  `creator_id` bypass, so it stays out of this change.

## Unit 9 run log — after the rate-limit change

Everything was run three separate times. Each run started a **fresh server**
(so rate-limit counts began at zero) and did four things in order, with the real
gpt2 model and the real rate limits:

1. `python run_attacks.py --flood 15`: 15 submissions from one `creator_id`.
2. `python run_eval.py --trials 1`: criteria 1 to 5 against the live server.
3. `GET /log`: the server's log, saved.
4. `python -m unittest -v test_rate_limit test_failures`: criteria 6 to 11.

The server for each run wrote to its own audit file, so none of this touched
`logs/audit.jsonl`. Everything is saved under `results/unit9_runs/`
(`run<N>_flood.txt`, `run<N>_eval.txt`, `run<N>_audit.jsonl`, `run<N>_tests.txt`,
`run<N>_log_endpoint.json`, `run<N>_server.log`) and in the three
`results/run_*_unit9_run<N>.md` reports, which hold the full JSON that came back.

| Criterion                            | Target                                                                              | Run 1                                                 | Run 2                       | Run 3                       | Verdict                                                      |
| ------------------------------------ | ----------------------------------------------------------------------------------- | ----------------------------------------------------- | --------------------------- | --------------------------- | ------------------------------------------------------------ |
| 1. False positives                   | none of 5 of my own pieces labelled `ai`                                            | MET (5 × `unsure`)                                    | MET (5 × `unsure`)          | MET (5 × `unsure`)          | MET                                                          |
| 2. Score spread                      | at least 4 of 5 AI/human pairs, AI ≥ 0.2 higher                                     | 2 of 2 pairs (0.496, 0.284)                           | 2 of 2 pairs (0.496, 0.284) | 2 of 2 pairs (0.496, 0.284) | **NOT FULLY TESTED**: only 2 pairs exist, the target needs 5 |
| 3. Label coverage                    | all of `ai`, `human`, `unsure` appear, nothing else                                 | MET (`ai`, `human`, `unsure`)                         | MET                         | MET                         | MET                                                          |
| 4. Appeal path                       | 5/5 appeals `under_review`, logged after the decision; unknown id errors            | MET (5/5; unknown id 404)                             | MET                         | MET                         | MET                                                          |
| 5. Bad input                         | 5 bad inputs: 4xx + `error`, logged, no label                                       | MET (400, 400, 400, 400, 413; 5 logged)               | MET                         | MET                         | MET                                                          |
| 6. Rotating `creator_id`             | 40 requests → 20 × `200`, 20 × `429`                                                | MET (20 / 20)                                         | MET (20 / 20)               | MET (20 / 20)               | MET                                                          |
| 7. One `creator_id`                  | 40 requests → 5 × `200`, 35 × `429`                                                 | MET (5 / 35); live flood of 15: 5 × `200`, 10 × `429` | MET (5 / 35); flood 5 / 10  | MET (5 / 35); flood 5 / 10  | MET                                                          |
| 8. Shared address                    | 4 writers × 5 requests, all `200`                                                   | MET                                                   | MET                         | MET                         | MET                                                          |
| 9. `429` tells caller how to recover | `Retry-After` 1 to 61, matching body, correct `scope`, `evaluated: false`, no label | MET (both scopes)                                     | MET                         | MET                         | MET                                                          |
| 10. Every `429` recorded             | `rate_limited` entries = number of `429`s                                           | MET (20 = 20, 35 = 35)                                | MET                         | MET                         | MET                                                          |
| 11. Service failure handled          | `503`/`500`, `evaluated: false`, `error` record, no decision, recovers              | MET (7 of 7 tests)                                    | MET (7 of 7)                | MET (7 of 7)                | MET                                                          |

**What the verdicts rest on.** Criteria 1 to 5 are judged from the eval output
and the run's own audit file. Criteria 6 to 11 are judged from the 14 tests,
which passed in all three runs (`Ran 14 tests`, `OK`). Criterion 7 was also
seen on the live server: the flood sent 15 requests and got 5 × `200` then
10 × `429` in every run.

**Things I should not hide:**

- **Criterion 2 is not really tested.** The criterion asks for 5 AI/human pairs.
  `scenarios.py` sends 3 texts: one AI, one human and one lightly edited AI, so
  there are only 2 pairs. Both clear 0.2 (0.781 against 0.285 is 0.496, and the
  edited AI at 0.569 against 0.285 is 0.284). That is 2 of 2, but I can't claim
  "at least 4 of 5". The Unit 8 table above marks this criterion MET on the same
  data; I don't think that was fully justified. It needs three more pairs.
- **Identical scores in all three runs.** Every score matched to four decimals
  across runs, so the model signal was deterministic here. The warning that
  identical input can score differently twice did not show up on this machine.
  Three runs is also a small sample.
- **Criterion 1 passes narrowly.** All five of my own pieces came out `unsure`
  and none `ai`, which is what the target asks, but none was confidently
  `human`.
- **The address cap interrupted the eval, and the run script waited it out.**
  The flood plus the eval send more than 20 requests from one address in a
  minute. In every run the second eval request ("Technology plays an important
  role...", criterion 2) got a `429` with `scope: "address"` and the script
  waited 50 to 51 s for `Retry-After`, then resent it. Each run's audit file
  therefore has 11 `rate_limited` entries: the flood's 10 plus that one. This is
  recorded as `retried_429` in the eval JSON. `run_eval.py` didn't do this
  before; I added it so the address cap doesn't hide the answers.
- **A first attempt was thrown away.** The first three runs went to a different
  server already running on port 5000, so they were not fresh and wrote to the
  real audit log. I deleted that output, removed the extra lines it added to
  `logs/audit.jsonl`, and redid all three on port 5055. Nothing above comes from
  that attempt.

**Real output, run 1.** The flood against the live server (runs 2 and 3 are the
same):

```
15 submissions as 'flood_tester' against http://127.0.0.1:5055

  [ 1/15] 200
  [ 2/15] 200
  [ 3/15] 200
  [ 4/15] 200
  [ 5/15] 200
  [ 6/15] 429
  [ 7/15] 429
  [ 8/15] 429
  [ 9/15] 429
  [10/15] 429
  [11/15] 429
  [12/15] 429
  [13/15] 429
  [14/15] 429
  [15/15] 429

10 of 15 were rate limited.
```

The eval, as it printed (`run_eval.py --trials 1`). All three runs printed the
same, with the wait of 50 to 51 s:

```
False positives  (criterion 1)
  trial 1: unsure, unsure, unsure, unsure, unsure
score spread  (criterion 2)
    429 on 'Technology plays an important ' - waiting 51s (retry 1)
  trial 1: ai, human, unsure
label coverage  (criterion 3)
  trial 1: ai, human, unsure
appeal path  (criterion 4)
  trial 1: unsure, unsure, unsure, unsure, unsure, —
bad input  (criterion 5)
  trial 1: —, —, —, —, —
```

(The `—` in the bad-input line is correct: those requests were refused, so there
is no guess. The `—` at the end of the appeal line is the made-up content id.)

The one `429` the eval hit, as logged in run 1's audit file:

```json
{
  "timestamp": "2026-11-16T22:31:52+00:00",
  "creator_id": "eval_score spread_1",
  "event": "rejected",
  "status": "rejected",
  "reason": "rate_limited",
  "limit": "20 per 1 minute",
  "scope": "address",
  "retry_after": 51,
  "duration_ms": 0.9,
  "input_chars": 400,
  "input_preview": "Technology plays an important role in modern education. It helps students learn new skills and acces"
}
```

The test output, run 1 (criteria 6 to 11; runs 2 and 3 matched, `Ran 14 tests`, `OK`):

```
test_429_tells_the_caller_how_to_recover (test_rate_limit.RateLimitTests.test_429_tells_the_caller_how_to_recover)
A 429 carries Retry-After, a structured body, and says nothing was evaluated. ... ok
test_address_limit_is_reported_as_address_scope (test_rate_limit.RateLimitTests.test_address_limit_is_reported_as_address_scope) ... ok
test_every_429_has_exactly_one_audit_record (test_rate_limit.RateLimitTests.test_every_429_has_exactly_one_audit_record)
Criterion 10: rejections and records match 1:1, in both flows. ... ok
test_rejection_is_audited_with_retry_after (test_rate_limit.RateLimitTests.test_rejection_is_audited_with_retry_after) ... ok
test_rotating_creator_id_from_one_address_is_limited (test_rate_limit.RateLimitTests.test_rotating_creator_id_from_one_address_is_limited)
A stranger rotating creator_id from ONE address must hit a 429. ... ok
test_single_creator_id_is_limited (test_rate_limit.RateLimitTests.test_single_creator_id_is_limited)
Control: the existing per-creator limit still works. ... ok
test_writers_sharing_an_address_are_not_punished (test_rate_limit.RateLimitTests.test_writers_sharing_an_address_are_not_punished)
Four real writers behind one address, each within their own limit. ... ok
test_a_failure_leaves_no_decision_to_appeal (test_failures.FailurePathTests.test_a_failure_leaves_no_decision_to_appeal) ... ok
test_detector_unavailable_is_a_503 (test_failures.FailurePathTests.test_detector_unavailable_is_a_503) ... ok
test_error_detail_stays_in_the_log_not_the_response (test_failures.FailurePathTests.test_error_detail_stays_in_the_log_not_the_response) ... ok
test_every_failure_leaves_an_error_record (test_failures.FailurePathTests.test_every_failure_leaves_an_error_record) ... ok
test_input_with_no_readable_words_is_refused_not_scored (test_failures.FailurePathTests.test_input_with_no_readable_words_is_refused_not_scored) ... ok
test_service_recovers_after_a_failure (test_failures.FailurePathTests.test_service_recovers_after_a_failure) ... ok
test_unexpected_exception_is_a_500_with_no_verdict (test_failures.FailurePathTests.test_unexpected_exception_is_a_500_with_no_verdict) ... ok

----------------------------------------------------------------------
Ran 14 tests in 0.308s

OK

  rotating creator_id x40: 20 x 200, 20 x 429
```

---

## Real output for each criterion, run 1

#### Criterion 1 — False positives

**Responses:** produced by `run_eval.py::main` (which sends the request) calling
`app.py::submit`. None is `ai`.

```json
[
  {
    "status": 200,
    "error": null,
    "appeal": null,
    "guess": "unsure",
    "confidence": 0.64,
    "model_score": 0.7193,
    "style_score": 0.5977,
    "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
    "retried_429": 0,
    "sent": "Good day,Unfortunately due to competing priorities, I will not be able"
  },
  {
    "status": 200,
    "error": null,
    "appeal": null,
    "guess": "unsure",
    "confidence": 0.3662,
    "model_score": 0.3311,
    "style_score": 0.4014,
    "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
    "retried_429": 0,
    "sent": "Hello, I am reaching out because a Walmart grocery delivery intended f"
  },
  {
    "status": 200,
    "error": null,
    "appeal": null,
    "guess": "unsure",
    "confidence": 0.6072,
    "model_score": 0.7719,
    "style_score": 0.4425,
    "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
    "retried_429": 0,
    "sent": "Hi Diana, Thank you for following up with me. I realized that I do not"
  },
  {
    "status": 200,
    "error": null,
    "appeal": null,
    "guess": "unsure",
    "confidence": 0.504,
    "model_score": 0.5451,
    "style_score": 0.463,
    "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
    "retried_429": 0,
    "sent": "Hello CS7 Students, Congratulations again on completing this class! We"
  },
  {
    "status": 200,
    "error": null,
    "appeal": null,
    "guess": "unsure",
    "confidence": 0.5282,
    "model_score": 0.4743,
    "style_score": 0.5821,
    "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
    "retried_429": 0,
    "sent": "The art of our mindset determines the people we become, directs the wa"
  }
]
```

**Log lines:** written by `audit.py::log_decision`, called from `app.py::submit`
(from `results/unit9_runs/run1_audit.jsonl`).

```json
{"timestamp": "2026-11-16T22:31:51+00:00", "content_id": "443e6b8e-fd46-40d2-96b4-f1c7720a7f25", "creator_id": "eval_False positi_1", "guess": "unsure", "model_score": 0.7193, "style_score": 0.5977, "combined_score": 0.64, "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.", "status": "decided", "model_ms": 115.4, "style_ms": 0.2, "duration_ms": 116.3, "input_chars": 205, "input_preview": "Good day,Unfortunately due to competing priorities, I will not be able to volunteer for the June sum"}
{"timestamp": "2026-11-16T22:31:51+00:00", "content_id": "164a8947-72b0-4c88-8e97-4f3621fe3583", "creator_id": "eval_False positi_2", "guess": "unsure", "model_score": 0.3311, "style_score": 0.4014, "combined_score": 0.3662, "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.", "status": "decided", "model_ms": 391.4, "style_ms": 0.4, "duration_ms": 392.8, "input_chars": 654, "input_preview": "Hello, I am reaching out because a Walmart grocery delivery intended for my residence at Windsor by "}
{"timestamp": "2026-11-16T22:31:51+00:00", "content_id": "cc62b71e-93f7-4724-84fe-25964e5c684d", "creator_id": "eval_False positi_3", "guess": "unsure", "model_score": 0.7719, "style_score": 0.4425, "combined_score": 0.6072, "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.", "status": "decided", "model_ms": 173.3, "style_ms": 0.3, "duration_ms": 174.9, "input_chars": 197, "input_preview": "Hi Diana, Thank you for following up with me. I realized that I do not meet the GPA requirement, I h"}
{"timestamp": "2026-11-16T22:31:52+00:00", "content_id": "33067a93-e1f4-4626-824a-9c817be3da6f", "creator_id": "eval_False positi_4", "guess": "unsure", "model_score": 0.5451, "style_score": 0.463, "combined_score": 0.504, "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.", "status": "decided", "model_ms": 204.9, "style_ms": 0.3, "duration_ms": 206.2, "input_chars": 496, "input_preview": "Hello CS7 Students, Congratulations again on completing this class! We are so proud of all you've ac"}
{"timestamp": "2026-11-16T22:31:52+00:00", "content_id": "33558df8-cac1-46e9-a698-76ec13d58602", "creator_id": "eval_False positi_5", "guess": "unsure", "model_score": 0.4743, "style_score": 0.5821, "combined_score": 0.5282, "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.", "status": "decided", "model_ms": 521.2, "style_ms": 0.3, "duration_ms": 522.5, "input_chars": 1193, "input_preview": "The art of our mindset determines the people we become, directs the way we live and thus what we pro"}
```

#### Criterion 2 — Score spread

**Responses:** `run_eval.py::main` calling `app.py::submit`. Combined scores are
`confidence`: 0.781 (AI), 0.2854 (human), 0.5693 (lightly edited AI).

```json
[
  {
    "status": 200,
    "error": null,
    "appeal": null,
    "guess": "ai",
    "confidence": 0.781,
    "model_score": 0.8579,
    "style_score": 0.7041,
    "label": "This looks like it may have been written by AI. We can get this wrong. If you wrote it yourself, you can appeal and ask for a person to look at it.",
    "retried_429": 1,
    "sent": "Technology plays an important role in modern education. It helps stude"
  },
  {
    "status": 200,
    "error": null,
    "appeal": null,
    "guess": "human",
    "confidence": 0.2854,
    "model_score": 0.3099,
    "style_score": 0.2609,
    "label": "We think this was probably written by a person.",
    "retried_429": 0,
    "sent": "Okay so \u2014 the dog ate my sandwich. Not a metaphor. Actual sandwich, ac"
  },
  {
    "status": 200,
    "error": null,
    "appeal": null,
    "guess": "unsure",
    "confidence": 0.5693,
    "model_score": 0.6698,
    "style_score": 0.4688,
    "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
    "retried_429": 0,
    "sent": "Remote work has changed how many people think about their jobs. It off"
  }
]
```

**Log lines:** `audit.py::log_decision`, called from `app.py::submit`. The `429`
on the first one is the address cap, and its record is under Criterion 9.

```json
{"timestamp": "2026-11-16T22:31:52+00:00", "creator_id": "eval_score spread_1", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "20 per 1 minute", "scope": "address", "retry_after": 51, "duration_ms": 0.9, "input_chars": 400, "input_preview": "Technology plays an important role in modern education. It helps students learn new skills and acces"}
{"timestamp": "2026-11-16T22:32:43+00:00", "content_id": "505eb1e8-454d-44cc-b348-7492da67b60d", "creator_id": "eval_score spread_1", "guess": "ai", "model_score": 0.8579, "style_score": 0.7041, "combined_score": 0.781, "label": "This looks like it may have been written by AI. We can get this wrong. If you wrote it yourself, you can appeal and ask for a person to look at it.", "status": "decided", "model_ms": 145.4, "style_ms": 0.3, "duration_ms": 146.6, "input_chars": 400, "input_preview": "Technology plays an important role in modern education. It helps students learn new skills and acces"}
{"timestamp": "2026-11-16T22:32:43+00:00", "content_id": "a867f493-a118-4a4f-86cd-ba43dc6f052b", "creator_id": "eval_score spread_2", "guess": "human", "model_score": 0.3099, "style_score": 0.2609, "combined_score": 0.2854, "label": "We think this was probably written by a person.", "status": "decided", "model_ms": 121.2, "style_ms": 0.3, "duration_ms": 122.2, "input_chars": 244, "input_preview": "Okay so — the dog ate my sandwich. Not a metaphor. Actual sandwich, actual dog (Biscuit, a menace). "}
{"timestamp": "2026-11-16T22:32:43+00:00", "content_id": "30c287cb-13b6-49d9-8270-772b86fe7472", "creator_id": "eval_score spread_3", "guess": "unsure", "model_score": 0.6698, "style_score": 0.4688, "combined_score": 0.5693, "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.", "status": "decided", "model_ms": 143.4, "style_ms": 0.2, "duration_ms": 144.4, "input_chars": 351, "input_preview": "Remote work has changed how many people think about their jobs. It offers flexibility and saves comm"}
```

#### Criterion 3 — Label coverage

**Responses:** `run_eval.py::main` calling `app.py::submit`. All three labels
appear: `ai`, `human`, `unsure`.

```json
[
  {
    "status": 200,
    "error": null,
    "appeal": null,
    "guess": "ai",
    "confidence": 0.781,
    "model_score": 0.8579,
    "style_score": 0.7041,
    "label": "This looks like it may have been written by AI. We can get this wrong. If you wrote it yourself, you can appeal and ask for a person to look at it.",
    "retried_429": 0,
    "sent": "Technology plays an important role in modern education. It helps stude"
  },
  {
    "status": 200,
    "error": null,
    "appeal": null,
    "guess": "human",
    "confidence": 0.2854,
    "model_score": 0.3099,
    "style_score": 0.2609,
    "label": "We think this was probably written by a person.",
    "retried_429": 0,
    "sent": "Okay so \u2014 the dog ate my sandwich. Not a metaphor. Actual sandwich, ac"
  },
  {
    "status": 200,
    "error": null,
    "appeal": null,
    "guess": "unsure",
    "confidence": 0.5693,
    "model_score": 0.6698,
    "style_score": 0.4688,
    "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
    "retried_429": 0,
    "sent": "Remote work has changed how many people think about their jobs. It off"
  }
]
```

**Log lines:** `audit.py::log_decision`, called from `app.py::submit`.

```json
{"timestamp": "2026-11-16T22:32:44+00:00", "content_id": "a3c6341a-f7eb-4a9c-9f76-e1ea2f4eb63c", "creator_id": "eval_label covera_1", "guess": "ai", "model_score": 0.8579, "style_score": 0.7041, "combined_score": 0.781, "label": "This looks like it may have been written by AI. We can get this wrong. If you wrote it yourself, you can appeal and ask for a person to look at it.", "status": "decided", "model_ms": 139.8, "style_ms": 0.2, "duration_ms": 140.9, "input_chars": 400, "input_preview": "Technology plays an important role in modern education. It helps students learn new skills and acces"}
{"timestamp": "2026-11-16T22:32:44+00:00", "content_id": "a8c906c0-1ce4-49dc-88b3-29cf50293526", "creator_id": "eval_label covera_2", "guess": "human", "model_score": 0.3099, "style_score": 0.2609, "combined_score": 0.2854, "label": "We think this was probably written by a person.", "status": "decided", "model_ms": 125.3, "style_ms": 0.2, "duration_ms": 126.3, "input_chars": 244, "input_preview": "Okay so — the dog ate my sandwich. Not a metaphor. Actual sandwich, actual dog (Biscuit, a menace). "}
{"timestamp": "2026-11-16T22:32:44+00:00", "content_id": "bbef22f7-7edf-41fe-be50-76c3fcc62a99", "creator_id": "eval_label covera_3", "guess": "unsure", "model_score": 0.6698, "style_score": 0.4688, "combined_score": 0.5693, "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.", "status": "decided", "model_ms": 158.9, "style_ms": 0.3, "duration_ms": 159.9, "input_chars": 351, "input_preview": "Remote work has changed how many people think about their jobs. It offers flexibility and saves comm"}
```

#### Criterion 4 — Appeal path

**Responses:** `run_eval.py::main` calling `app.py::submit`, then
`run_eval.py::appeal_for` calling `app.py::appeal`. The last entry is the
made-up content id, which returns `404 unknown_content_id`.

```json
[
  {
    "status": 200,
    "error": null,
    "appeal": {
      "status": 200,
      "body_status": "under_review",
      "error": null
    },
    "guess": "unsure",
    "confidence": 0.4306,
    "model_score": 0.461,
    "style_score": 0.4002,
    "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
    "retried_429": 0,
    "sent": "Good day, due to competing priorities I will not be able to volunteer "
  },
  {
    "status": 200,
    "error": null,
    "appeal": {
      "status": 200,
      "body_status": "under_review",
      "error": null
    },
    "guess": "unsure",
    "confidence": 0.5162,
    "model_score": 0.6372,
    "style_score": 0.3952,
    "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
    "retried_429": 0,
    "sent": "Hi Diana, thank you for following up. I do not meet the GPA requiremen"
  },
  {
    "status": 200,
    "error": null,
    "appeal": {
      "status": 200,
      "body_status": "under_review",
      "error": null
    },
    "guess": "unsure",
    "confidence": 0.3715,
    "model_score": 0.3451,
    "style_score": 0.3978,
    "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
    "retried_429": 0,
    "sent": "Okay so, the dog ate my sandwich. Not a metaphor. I turned around for "
  },
  {
    "status": 200,
    "error": null,
    "appeal": {
      "status": 200,
      "body_status": "under_review",
      "error": null
    },
    "guess": "unsure",
    "confidence": 0.64,
    "model_score": 0.7691,
    "style_score": 0.5834,
    "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
    "retried_429": 0,
    "sent": "Remote work has changed how many people think about their jobs. It off"
  },
  {
    "status": 200,
    "error": null,
    "appeal": {
      "status": 200,
      "body_status": "under_review",
      "error": null
    },
    "guess": "unsure",
    "confidence": 0.64,
    "model_score": 0.8341,
    "style_score": 0.6143,
    "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
    "retried_429": 0,
    "sent": "Technology plays an important role in modern education. It helps stude"
  },
  {
    "sent": "(unknown content_id)",
    "appeal": {
      "status": 404,
      "body_status": null,
      "error": "unknown_content_id"
    }
  }
]
```

**Log lines:** the appeals as written by `audit.py::log_appeal`, called from
`app.py::appeal`. Each one sits after its original decision in the file, and the
decision line is unchanged.

```json
{"timestamp": "2026-11-16T22:32:44+00:00", "content_id": "99e45114-1638-412d-87db-9743a72a5493", "creator_id": "eval_appeal path_1", "event": "appeal", "status": "under_review", "reasoning": "These are formal emails I wrote myself and the decision is wrong."}
{"timestamp": "2026-11-16T22:32:44+00:00", "content_id": "4f4a354d-0b5e-4310-9e24-6dc808e3d3e7", "creator_id": "eval_appeal path_2", "event": "appeal", "status": "under_review", "reasoning": "These are formal emails I wrote myself and the decision is wrong."}
{"timestamp": "2026-11-16T22:32:44+00:00", "content_id": "5571f342-31d5-46f9-9d3b-af8b2b187e16", "creator_id": "eval_appeal path_3", "event": "appeal", "status": "under_review", "reasoning": "These are formal emails I wrote myself and the decision is wrong."}
{"timestamp": "2026-11-16T22:32:44+00:00", "content_id": "6fa25280-b6ac-42ef-81c2-f42dabaa1491", "creator_id": "eval_appeal path_4", "event": "appeal", "status": "under_review", "reasoning": "These are formal emails I wrote myself and the decision is wrong."}
{"timestamp": "2026-11-16T22:32:44+00:00", "content_id": "12e357f6-14ab-4e83-91de-16527967e6ed", "creator_id": "eval_appeal path_5", "event": "appeal", "status": "under_review", "reasoning": "These are formal emails I wrote myself and the decision is wrong."}
```

#### Criterion 5 — Bad input

**Responses:** `run_eval.py::main` calling `app.py::submit`. Every one is a 4xx
with an `error` field and no label.

```json
[
  {
    "status": 400,
    "error": "missing_text",
    "appeal": null,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "retried_429": 0,
    "sent": "{\"creator_id\": \"eval_bad_missing\"}"
  },
  {
    "status": 400,
    "error": "missing_text",
    "appeal": null,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "retried_429": 0,
    "sent": "{\"text\": null, \"creator_id\": \"eval_bad_null\"}"
  },
  {
    "status": 400,
    "error": "empty_text",
    "appeal": null,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "retried_429": 0,
    "sent": "(empty text)"
  },
  {
    "status": 400,
    "error": "empty_text",
    "appeal": null,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "retried_429": 0,
    "sent": "   \n\t  "
  },
  {
    "status": 413,
    "error": "text_too_long",
    "appeal": null,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "retried_429": 0,
    "sent": "word word word word word word word word word word word word word word "
  }
]
```

**Log lines:** `audit.py::log_rejection`, called from `app.py::_reject`.

```json
{"timestamp": "2026-11-16T22:32:44+00:00", "creator_id": "eval_bad_missing", "event": "rejected", "status": "rejected", "reason": "missing_text", "http_status": 400, "duration_ms": 0.7, "input_chars": null, "input_preview": null}
{"timestamp": "2026-11-16T22:32:44+00:00", "creator_id": "eval_bad_null", "event": "rejected", "status": "rejected", "reason": "missing_text", "http_status": 400, "duration_ms": 0.3, "input_chars": null, "input_preview": null}
{"timestamp": "2026-11-16T22:32:44+00:00", "creator_id": "eval_bad_empty", "event": "rejected", "status": "rejected", "reason": "empty_text", "http_status": 400, "duration_ms": 0.4, "input_chars": 0, "input_preview": ""}
{"timestamp": "2026-11-16T22:32:44+00:00", "creator_id": "eval_bad_whitespace", "event": "rejected", "status": "rejected", "reason": "empty_text", "http_status": 400, "duration_ms": 0.4, "input_chars": 7, "input_preview": "   \n\t  "}
{"timestamp": "2026-11-16T22:32:44+00:00", "creator_id": "eval_bad_huge", "event": "rejected", "status": "rejected", "reason": "text_too_long", "http_status": 413, "length": 5500, "duration_ms": 0.8, "input_chars": 5500, "input_preview": "word word word word word word word word word word word word word word word word word word word word "}
```

#### Criterion 6 — Rotating `creator_id` does not bypass the limit

Printed by `test_rate_limit.py::RateLimitTests.test_rotating_creator_id_from_one_address_is_limited`
(40 requests, a new `creator_id` each, one address), from `run1_tests.txt`:

```
test_rotating_creator_id_from_one_address_is_limited (test_rate_limit.RateLimitTests.test_rotating_creator_id_from_one_address_is_limited)
A stranger rotating creator_id from ONE address must hit a 429. ... ok

  rotating creator_id x40: 20 x 200, 20 x 429
```

The `rotating creator_id x40` line is printed by that test (it prints after the
other tests' results, as the last line of the file).

#### Criterion 7 — One `creator_id` is still held to its own limit

Against the live server: `run_attacks.py::run_flood`, 15 submissions as
`flood_tester`, from `run1_flood.txt`:

```
  [ 1/15] 200
  [ 2/15] 200
  [ 3/15] 200
  [ 4/15] 200
  [ 5/15] 200
  [ 6/15] 429
  [ 7/15] 429
  [ 8/15] 429
  [ 9/15] 429
  [10/15] 429
  [11/15] 429
  [12/15] 429
  [13/15] 429
  [14/15] 429
  [15/15] 429

============================================================
```

The unit test `test_rate_limit.py::RateLimitTests.test_single_creator_id_is_limited`
asserts 5 × `200` and 35 × `429` for 40 requests:

```
test_single_creator_id_is_limited (test_rate_limit.RateLimitTests.test_single_creator_id_is_limited)
Control: the existing per-creator limit still works. ... ok
```

#### Criterion 8 — Writers who share an address are not punished

From `run1_tests.txt`, produced by
`test_rate_limit.py::RateLimitTests.test_writers_sharing_an_address_are_not_punished`
(it asserts that all 20 requests got `200`; the test output only records the
pass, it does not save the 20 responses):

```
test_writers_sharing_an_address_are_not_punished (test_rate_limit.RateLimitTests.test_writers_sharing_an_address_are_not_punished)
Four real writers behind one address, each within their own limit. ... ok
```

#### Criterion 9 — Every `429` tells the caller how to recover

The live-server 429 records, written by `audit.py::log_rejection` from the
`429` handler `app.py::rate_limited` (from `run1_audit.jsonl`). First the
per-creator one from the flood, then the address-scope one the eval hit:

```json
{"timestamp": "2026-11-16T22:31:50+00:00", "creator_id": "flood_tester", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "5 per 1 minute", "scope": "creator", "retry_after": 53, "duration_ms": 0.8, "input_chars": 148, "input_preview": "This is an ordinary submission, sent over and over from the same account to find out where the rate "}
{"timestamp": "2026-11-16T22:31:52+00:00", "creator_id": "eval_score spread_1", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "20 per 1 minute", "scope": "address", "retry_after": 51, "duration_ms": 0.9, "input_chars": 400, "input_preview": "Technology plays an important role in modern education. It helps students learn new skills and acces"}
```

The response header and body are asserted by
`test_rate_limit.py::RateLimitTests.test_429_tells_the_caller_how_to_recover` and
`test_address_limit_is_reported_as_address_scope`, which passed in run 1:

```
test_429_tells_the_caller_how_to_recover (test_rate_limit.RateLimitTests.test_429_tells_the_caller_how_to_recover)
A 429 carries Retry-After, a structured body, and says nothing was evaluated. ... ok
test_address_limit_is_reported_as_address_scope (test_rate_limit.RateLimitTests.test_address_limit_is_reported_as_address_scope) ... ok
```

The run did not save a live 429 response body, so the body itself is only shown
by those assertions, not pasted.

#### Criterion 10 — Every `429` leaves a record

In run 1 the flood saw 10 × `429` (`run_attacks.py::run_flood`) and the eval saw
1 × `429` and retried it (`run_eval.py::main`, "waiting 51s"). That is 11, and
`audit.py::log_rejection` wrote this many `rate_limited` lines to
`run1_audit.jsonl`:

```
$ grep -c '"reason": "rate_limited"' results/unit9_runs/run1_audit.jsonl
11
```

The exact-match assertion over the 40-request flows is
`test_rate_limit.py::RateLimitTests.test_every_429_has_exactly_one_audit_record`:

```
test_every_429_has_exactly_one_audit_record (test_rate_limit.RateLimitTests.test_every_429_has_exactly_one_audit_record)
Criterion 10: rejections and records match 1:1, in both flows. ... ok
test_rejection_is_audited_with_retry_after (test_rate_limit.RateLimitTests.test_rejection_is_audited_with_retry_after) ... ok
```

#### Criterion 11 — Service failure is handled

The two tests that cause the failure write to a temporary log that is deleted
afterwards, so run 1 has no saved failure _log lines_. What run 1 saved is the
result of the tests, from `test_failures.py::FailurePathTests`:

```
test_unexpected_exception_is_a_500_with_no_verdict (test_failures.FailurePathTests.test_unexpected_exception_is_a_500_with_no_verdict) ... ok
test_detector_unavailable_is_a_503 (test_failures.FailurePathTests.test_detector_unavailable_is_a_503) ... ok
test_error_detail_stays_in_the_log_not_the_response (test_failures.FailurePathTests.test_error_detail_stays_in_the_log_not_the_response) ... ok
test_every_failure_leaves_an_error_record (test_failures.FailurePathTests.test_every_failure_leaves_an_error_record) ... ok
test_a_failure_leaves_no_decision_to_appeal (test_failures.FailurePathTests.test_a_failure_leaves_no_decision_to_appeal) ... ok
test_service_recovers_after_a_failure (test_failures.FailurePathTests.test_service_recovers_after_a_failure) ... ok
test_input_with_no_readable_words_is_refused_not_scored (test_failures.FailurePathTests.test_input_with_no_readable_words_is_refused_not_scored) ... ok
```

The actual log lines for these failures come from `measure_cost.py` (an earlier
run, not one of the three), which induced the same failures against the real
service and wrote them with `audit.py::log_error` and `audit.py::log_rejection`
(from `app.py::_unexpected_error` and `app.py::_reject`) into
`logs/instrumentation_run.jsonl`:

```json
{"timestamp": "2026-11-16T21:28:21+00:00", "creator_id": "fail_emoji", "event": "rejected", "status": "rejected", "reason": "no_readable_text", "http_status": 422, "duration_ms": 0.8, "input_chars": 7, "input_preview": "🙂🙂🙂 ???"}
{"timestamp": "2026-11-16T21:28:21+00:00", "creator_id": "fail_detector", "event": "error", "status": "error", "reason": "detector_unavailable", "http_status": 503, "error_type": "DetectorUnavailable", "error_message": "model files missing", "path": "/submit", "duration_ms": 0.7, "input_chars": 400, "input_preview": "Technology plays an important role in modern education. It helps students learn new skills and acces"}
{"timestamp": "2026-11-16T21:28:21+00:00", "creator_id": "fail_crash", "event": "error", "status": "error", "reason": "internal_error", "http_status": 500, "error_type": "RuntimeError", "error_message": "simulated crash in signal one", "path": "/submit", "duration_ms": 0.4, "input_chars": 400, "input_preview": "Technology plays an important role in modern education. It helps students learn new skills and acces"}
```

---

## Capstone

### How I Used AI

**Moment 1 — Hardening the rate-limit failure**

- _What I asked for:_ One way to harden the system when it hits the rate limit,
  and a better way for it to respond. Then I asked for the change and a test.
- _What came back:_ It read `app.py` first and said the 429 handler already
  logged the rejection, but returned a flat "try again shortly". It proposed a
  `Retry-After` header, a body with `retry_after` and `scope`, and
  `evaluated: false` so a rejection can't be read as a verdict. It built that
  with three tests. One test failed (`Retry-After` came out as 61 on a 60-second
  window because the reset time is rounded up), and it relaxed the bound to 61
  and said so, instead of changing the behavior.
- _What I changed:_ I chose to have it implemented, then had the README and
  `RUNNING.md` updated to match. I kept the 61 bound because it was explained,
  but it is a known quirk, listed under What's Still Broken.

**Moment 2 — Logging, failures and the cost number**

- _What I asked for:_ Structured logging with named fields, failures logged,
  and a cost per run measured over ten runs, with ten entries and one failure
  pasted into the README.
- _What came back:_ Fields added to every record (`duration_ms`, `input_chars`,
  `input_preview`, and `model_ms` and `style_ms` per stage), an error handler so
  a crash leaves a record instead of a bare 500, and `measure_cost.py`, which
  times the real model with both a wall clock and CPU time. It measured 0.123 s
  wall and 0.455 s CPU, and said that CPU is higher because torch uses several
  threads. It also said plainly that the 500 and 503 records were induced by
  making the detector raise, not seen in the wild.
- _What I changed:_ I kept the cost in CPU-seconds, since there is no API spend,
  and I did the hundred-people arithmetic on top of the measured number.

**Moment 3 — Criteria and the three runs**

- _What I asked for:_ Five more criteria based on the rate-limit tests, then one
  about what happens when things go wrong, then everything run three separate
  times with the real output pasted.
- _What came back:_ Criteria 6 to 11, each tied to a test, and a new
  `test_failures.py` so the failure criterion rested on something checked. It
  said criterion 11 doesn't cover timeouts. When it ran the three runs, it
  noticed its own audit files were empty, found another server already on port 5000 that had
  taken all the requests and written to my real audit log, and threw those runs
  away. It removed the lines it had added and redid all three on another port. It
  also reported that criterion 2 only ever had 2 AI/human pairs, so my Unit 8
  "MET" for it wasn't fully justified.
- _What I changed:_ I asked for the real output for each criterion, and the log
  lines, to be pasted. I treated the criterion 2 finding as a real gap and listed
  it under What's Still Broken, and left my original criteria 1 to 5 untouched.

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
