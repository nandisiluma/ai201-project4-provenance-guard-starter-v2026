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

Two things worth knowing before you pick numbers:/.

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

<!--
UNIT 9: Additional criteria for improved rate-limiting
-->

# Unit 9 — rate-limiting criteria

Five more criteria, each one checked by a test in `test_rate_limit.py`. The
limits they refer to are in `config.py`: 5 per minute for one `creator_id`, and
20 per minute for one address. Each target has to hold in all 3 trials, with the
limiter reset between trials.

---

## 6. Rotating `creator_id` does not bypass the limit

40 submissions from one address, each with a different `creator_id`, get exactly
20 `200` responses and 20 `429` responses, in each of 3 trials.

**Why this target:**

This is the bug the unit fixes. Before the address cap, the same 40 requests all
got `200`, because the caller chose their own `creator_id` and every one counted
as a new writer. "Exactly 20" matters in both directions: more than 20 means the
bypass is still open, fewer means real requests were refused early.

---

## 7. One `creator_id` is still held to its own limit

40 submissions under one `creator_id` get exactly 5 `200` responses and 35 `429`
responses, in each of 3 trials.

**Why this target:**

The per-writer limit is the tighter of the two (5 against 20) and is what keeps
one person from hammering the model, which costs about 0.46 CPU-seconds a run.
Adding the address cap must not loosen it, so this is the control for criterion
6: if the address check quietly replaced the creator check, this would drop from
5 to 20 and I would see it.

---

## 8. Writers who share an address are not punished

4 different `creator_id`s from one address, each sending 5 submissions (the
per-writer limit), all 20 get `200`, with no `429`, in each of 3 trials.

**Why this target:**

A classroom or a household shares one address. Four writers each staying inside
their own limit have done nothing wrong, so none of them should be turned away
because of the others. Four writers at 5 each is 20, which sits exactly on the
address cap, so this also shows the cap is set high enough for a small group
and no higher.

---

## 9. Every `429` tells the caller how to recover

In 100% of `429` responses I sample, including one from each limit, the
response has a `Retry-After` header that is a whole number from 1 to 61. The
body has `error: "rate_limited"`, a `retry_after` equal to the header, `scope`
set to `creator` or `address` to match the limit that tripped, and
`evaluated: false`. The body has no `label` or `guess`.

**Why this target:**

A bare "try again shortly" makes a script retry at once and stay blocked, and
leaves a real writer not knowing how long to wait or which limit they hit. The
bigger risk is a rejection being read as a verdict: a text that was never scored
must not look like a text that was cleared, so `evaluated: false` with no label
is part of the target, not decoration. 61 is the upper bound because the reset
time is rounded up and measured at 61 for a one-minute window.

---

## 10. Every `429` leaves a record

In 3 trials of the 40-request runs above, the number of `rate_limited` entries
in the audit log equals the number of `429` responses (20 and 35), and each entry
has `scope`, `retry_after`, `duration_ms` and the `creator_id` sent. There are no
rejections without a record and no records without a rejection.

**Why this target:**

An attack that shows up only as an absence is one I would never find. A flood of
rejected requests that left no trace would look the same as a quiet afternoon.
The test only checks that one entry exists, so I set the stricter target of the
counts matching exactly: that is what shows no `429` slips through unlogged. I
checked it by hand and the counts match (20 of 20 and 35 of 35 in each trial);
`test_rate_limit.py` doesn't assert the equality yet.

---

## 11. When the service itself fails, it says so, stays honest and leaves a record

When signal one fails, both for a `DetectorUnavailable` (model missing or won't
load) and for an unexpected exception, in 3 trials of each:

- The response is a `503` (unavailable) or `500` (anything else) with an `error`
  field and `evaluated: false`.
- It carries no `label`, `guess`, `confidence` or score, and no exception text
  or traceback.
- The audit log gets one `error` entry with `creator_id`, `reason`,
  `http_status`, `error_type`, `error_message`, `duration_ms` and `input_chars`.
  The exception detail is in that entry, not in the response.
- No decision is logged, so there is nothing to appeal for a text that was never
  scored.
- The next valid submission afterwards gets a `200`, and `/ping` still answers.

Text with no readable words (emoji, punctuation, another script) is an empty
result and is refused with a `422` and a `no_readable_text` entry, never scored.

**Why this target:**

This is the path where the interesting failures live. A crash that returned a
plain 500 and left nothing behind would look to a writer like "no result" and to
me like a quiet afternoon. The worst version is a failure that comes back looking
like a verdict, so a text that was never read cannot carry a label. Keeping the
exception text out of the response stops a path or a secret from reaching a
stranger, while the log still gives me what I need to diagnose it. I include
recovery because a failure that leaves the service stuck is worse than one that
doesn't. Criterion 5 covers inputs the service refuses on sight. This one covers
what happens when the input was fine and the service broke.

Checked by `test_failures.py` (7 tests, all passing), where the failures are
induced by making `detector.model_signal` raise. **Not covered:** timeouts. The
service has no server-side time limit on scoring, so a request that hangs would
hang. Only the test scripts time out (90 s client side). That is a known gap, not
a criterion I can claim.
