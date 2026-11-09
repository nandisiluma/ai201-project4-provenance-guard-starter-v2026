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

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->

**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->

---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->

**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->

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

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
