# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. _"The
detector is accurate"_ is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. _"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"_ is a criterion.

Under each, write a sentence or two on **why that target**. _"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"_ is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area            | A question it could answer                                    |
| --------------- | ------------------------------------------------------------- |
| False positives | How often may a human's writing get called AI?                |
| Score spread    | How far apart should clearly-AI and clearly-human text score? |
| Label coverage  | Is every one of your three labels actually reachable?         |
| The appeal path | Does an appeal always change status and always get recorded?  |
| Bad input       | What happens when `text` is missing, empty, or enormous?      |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---

## 1.

<!-- Your criterion. It must name a number. -->

Of 5 pieces I wrote myself (at least 1 written plainly, in short sentences with common words), none is labelled `ai` in any of 3 trials.

**Why this target:**

Falsely accusing a person of using generated writing costs that writer a lot. I would rather miss some AI texts than wrongly accuse a human, so "unsure" is acceptable for human writing but `ai` is not. I include a plainly written piece because that is the writing the model signal is most likely to get wrong.

---

## 2.

<!-- Your criterion. -->

In at least 4 of 5 AI/human pairs, the combined score for the AI text is at least 0.2 higher than for the human text, in each of 3 trials.

**Why this target:**

I want to avoid coin-flip guesses as much as possible, and a 0.2 spread is a clear differentiator. It is also wide enough that a pair has a real chance of landing in different labels instead of both falling in the "unsure" band.

---

## 3.

<!-- Your criterion. -->

Across my test inputs, each of the three labels (`ai`, `human`, `unsure`) is produced at least once, and every valid input (1 to 5000 characters) gets one of them and nothing else.

**Why this target:**

A label that no input can produce means my score ranges have a gap, so a reader could never see it. I want every real submission to get an answer a person can read, and bad input is handled separately in criterion 5.

---

## 4.

<!-- Your criterion. -->

Every appeal on a valid `content_id` is recorded in the audit log with status `under_review`, appended after the original decision (which stays unchanged), in 5/5 test appeals. An appeal on an unknown `content_id` returns an error instead of being recorded as a valid appeal.

**Why this target:**

The appeal is the only thing between a wrong accusation and nothing at all, so a lost appeal means a writer was ignored and nobody can tell. The log has to show what was decided, that it was challenged, and in what order, so a reviewer can audit it later. I set 5 of 5 because I don't accept any silently dropped appeals.

---

## 5.

<!-- Your criterion. -->

Each of these 5 bad inputs gets a 4xx response with an `error` field and a rejection entry in `/log`, and none returns a 500 or a label: missing `text` key, `text` set to null, empty string, whitespace-only string, and text over 5000 characters. It is not scored or labelled.

**Why this target:**

A made-up label on input that isn't real text could read as an accusation against a writer, so the safest answer is to refuse and say why. A crash on malformed input is one of the most common real failures, and logging the rejection means a bad request still leaves a trace. AC 3 only covers valid input, so the two criteria don't conflict.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
