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

**Human**
'Effective communication is a cornerstone of successful teamwork. When team members share information openly, they build trust and foster collaboration. Furthermore, clear communication helps to minimize misunderstandings and ensures that everyone is aligned on goals. By actively listening and providing constructive feedback, individuals can contribute to a positive and productive work environment. In conclusion, prioritizing communication is essential for achieving long-term organizational success.'

**AI**
"Time management is an essential skill that helps students achieve their goals. By creating a consistent schedule, students can balance their academic responsibilities and personal interests. Furthermore, setting clear priorities allows individuals to use their time effectively and reduce stress."

**Formal Human**
The committee convened on Tuesday to consider the proposed amendments to the municipal zoning ordinance. After extended deliberation, it was resolved that the residential density limits would remain unchanged, pending a further review of infrastructure capacity. Several members expressed reservations regarding the projected burden on existing water and sewage services; these concerns will be addressed in the subsequent report, which is expected before the close of the fiscal year.

**Slightly-edited AI**
Remote work has changed how many people think about their jobs. It offers flexibility and saves commuting time, but it can also blur the line between work and home. Some people love it. Others miss the office more than they expected, honestly. Companies are still working out what a good balance looks like, and I suspect they will be for a while yet.

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label                 | Score range | The exact text a reader sees |
| --------------------- | ----------- | ---------------------------- |
| high-confidence human |             |                              |
| unsure                |             |                              |
| high-confidence AI    |             |                              |

**Why I worded the "unsure" one this way:**

<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->

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
  -d '{"text": "The weather is choppy", "creator_id": "A253"}'
```

```json
{
  "confidence": 0.5,
  "content_id": "857879b3-d5ef-41cb-b243-ddf714d4cf48",
  "guess": "unsure",
  "label": "PLACEHOLDER label",
  "model_score": 0.2013,
  "style_score": 0.5
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "857879b3-d5ef-41cb-b243-ddf714d4cf48", "reasoning": "testing"}'
```

```json
{
  "error": "not_implemented",
  "message": "POST /appeal isn't built yet \u2014 see the TODO in app.py.",
  "you_sent": {
    "content_id": "857879b3-d5ef-41cb-b243-ddf714d4cf48",
    "reasoning": "testing"
  }
}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json
{
  "count": 1,
  "entries": [
    {
      "combined_score": null,
      "content_id": "857879b3-d5ef-41cb-b243-ddf714d4cf48",
      "creator_id": "A253",
      "guess": "unsure",
      "label": "PLACEHOLDER label",
      "model_score": 0.2013,
      "status": "decided",
      "style_score": null,
      "timestamp": "2026-11-03T22:18:21+00:00"
    }
  ]
}
```

---

## How I Used AI

**Moment 1**

- _What I asked for:_
- _What came back:_
- _What I changed:_

**Moment 2**

- _What I asked for:_
- _What came back:_
- _What I changed:_

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** **_ per minute, _** per day

**Why those numbers and not others:**

<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->

**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
| --------- | ------ | ----- | ----- | ----- | ------- |
| 1.        |        |       |       |       |         |
| 2.        |        |       |       |       |         |
| 3.        |        |       |       |       |         |
| 4.        |        |       |       |       |         |
| 5.        |        |       |       |       |         |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

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
