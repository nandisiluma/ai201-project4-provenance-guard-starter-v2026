# Attack run — unit9_before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-16 11:24
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `e84d7520-b0c0-4211-860c-09eca0efaa87` | unsure | 0.386 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `95926314-aa54-4736-902c-a5e94db78a73` | unsure | 0.496 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `62acd4cb-89cf-4176-9906-e27d6e661284` | unsure | 0.575 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `a5837694-3f92-41a1-8b23-cd4dec7bf4f4` | unsure | 0.608 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `dff5d16c-f9ad-4716-af73-983ade5d8127` | unsure | 0.379 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `2af64b84-0067-4f27-922a-bcca0a1bb4f4` | unsure | 0.473 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `dc718411-88df-4bb3-8575-e463a34da7ef` | unsure | 0.383 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `c55dcc24-1522-4ff3-b66c-2951502f0d55` | unsure | 0.409 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `f58a2aab-aaf1-4f4a-92ec-761a2b9f10f5` | unsure | 0.603 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `401a9d6f-9026-45e2-9151-0816b176aeac` | ai | 0.871 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `c0e71328-bf86-40f9-8035-c646eb4322d9` | unsure | 0.602 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `0f2e3944-7ec1-455d-a0ff-4605e6cfb784` | unsure | 0.640 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `66bf7193-e615-49bc-aac0-6d21c3e053dd` | unsure | 0.640 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `691bf759-93f9-43e8-96bd-7d6e9c49160c` | unsure | 0.640 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `730d9515-ddc4-4eba-9b22-319ff887e3a3` | unsure | 0.640 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `af3b7f39-98bb-469e-8d53-3dcaba89df9d` | unsure | 0.640 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `98da8aa6-6736-4efb-bb76-4f8cd63f4142` | unsure | 0.640 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `0c1bba8f-47b9-4b17-bab0-2c9731bc7434` | unsure | 0.422 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `548e66a6-1380-4242-af70-bcea0b85d223` | unsure | 0.465 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `b7f4aed6-9c07-49f3-8673-f5b07010278d` | human | 0.305 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `4cb1e6b3-79f6-4cc3-8d75-698ce8c1b668` | unsure | 0.552 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `5d51a871-bd66-4a14-8fee-c06c022d6484` | unsure | 0.488 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `58fc25bb-b18b-4357-8389-d6d2b684e1be` | unsure | 0.414 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `ee39f9c0-78e5-4aff-9511-ce627e8a7831` | unsure | 0.575 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 422 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 200 | `87cc4496-aead-4d29-a608-ce349167a8af` | human | 0.250 |  |
| MF04 | malformed | text is only punctuation | 422 | `—` | — | — |  |
| MF05 | malformed | text is a very long single word | 200 | `a7f80f8b-a3f8-4b9d-a237-601ca731b7c3` | unsure | 0.640 |  |
| MF06 | malformed | text is emoji only | 422 | `—` | — | — |  |
| MF07 | malformed | text is right-to-left script | 422 | `—` | — | — |  |
| MF08 | malformed | text is 60,000 characters | 413 | `—` | — | — |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 200 | `48b7e469-549e-48a8-8f05-ffffbe8b881c` | unsure | 0.370 |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 200 | `39543ba4-88a9-43b4-9c0c-8e12dde6fce1` | human | 0.275 |  |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `fee43d6b-b4ec-4b71-ab65-f450523ec6f4` | human | 0.264 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `dfac3a3f-b936-41e2-b668-111e1016c334` | human | 0.264 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `465e8dd6-aaa1-4677-b925-a72075cc2e12` | human | 0.264 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `7cebaf55-2703-4f33-9ca4-205c9c34c258` | human | 0.264 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `bc60fd3f-654d-4422-bdc9-a25cbec5a646` | human | 0.264 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "e84d7520-b0c0-4211-860c-09eca0efaa87",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.3863,
  "model_score": 0.1635,
  "style_score": 0.6092,
  "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "95926314-aa54-4736-902c-a5e94db78a73",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.4963,
  "model_score": 0.5943,
  "style_score": 0.3983,
  "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "62acd4cb-89cf-4176-9906-e27d6e661284",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.5753,
  "model_score": 0.6662,
  "style_score": 0.4843,
  "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "a5837694-3f92-41a1-8b23-cd4dec7bf4f4",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.6081,
  "model_score": 0.6114,
  "style_score": 0.6048,
  "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "dff5d16c-f9ad-4716-af73-983ade5d8127",
  "creator_id": "attacker_EV05",
  "guess": "unsure",
  "confidence": 0.3793,
  "model_score": 0.3212,
  "style_score": 0.4375,
  "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "2af64b84-0067-4f27-922a-bcca0a1bb4f4",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.4729,
  "model_score": 0.5727,
  "style_score": 0.3732,
  "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "dc718411-88df-4bb3-8575-e463a34da7ef",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.3833,
  "model_score": 0.5862,
  "style_score": 0.1804,
  "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "c55dcc24-1522-4ff3-b66c-2951502f0d55",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.4088,
  "model_score": 0.2452,
  "style_score": 0.5724,
  "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "f58a2aab-aaf1-4f4a-92ec-761a2b9f10f5",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.603,
  "model_score": 0.7042,
  "style_score": 0.5018,
  "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "401a9d6f-9026-45e2-9151-0816b176aeac",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.8705,
  "model_score": 0.9792,
  "style_score": 0.7619,
  "label": "This looks like it may have been written by AI. We can get this wrong. If you wrote it yourself, you can appeal and ask for a person to look at it.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "c0e71328-bf86-40f9-8035-c646eb4322d9",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.6015,
  "model_score": 0.6175,
  "style_score": 0.5854,
  "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "0f2e3944-7ec1-455d-a0ff-4605e6cfb784",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.64,
  "model_score": 0.7387,
  "style_score": 0.6655,
  "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "66bf7193-e615-49bc-aac0-6d21c3e053dd",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.64,
  "model_score": 0.8051,
  "style_score": 0.6496,
  "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "691bf759-93f9-43e8-96bd-7d6e9c49160c",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.64,
  "model_score": 0.8329,
  "style_score": 0.5886,
  "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "730d9515-ddc4-4eba-9b22-319ff887e3a3",
  "creator_id": "attacker_FP05",
  "guess": "unsure",
  "confidence": 0.64,
  "model_score": 0.8005,
  "style_score": 0.6744,
  "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "af3b7f39-98bb-469e-8d53-3dcaba89df9d",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.64,
  "model_score": 0.8814,
  "style_score": 0.5613,
  "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "98da8aa6-6736-4efb-bb76-4f8cd63f4142",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.64,
  "model_score": 0.8816,
  "style_score": 0.5586,
  "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "0c1bba8f-47b9-4b17-bab0-2c9731bc7434",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.4223,
  "model_score": 0.3223,
  "style_score": 0.5223,
  "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "548e66a6-1380-4242-af70-bcea0b85d223",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.4653,
  "model_score": 0.4625,
  "style_score": 0.468,
  "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "b7f4aed6-9c07-49f3-8673-f5b07010278d",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.3046,
  "model_score": 0.2044,
  "style_score": 0.4049,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "4cb1e6b3-79f6-4cc3-8d75-698ce8c1b668",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.5521,
  "model_score": 0.5943,
  "style_score": 0.5099,
  "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "5d51a871-bd66-4a14-8fee-c06c022d6484",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.4877,
  "model_score": 0.4998,
  "style_score": 0.4756,
  "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "58fc25bb-b18b-4357-8389-d6d2b684e1be",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.4137,
  "model_score": 0.6401,
  "style_score": 0.1873,
  "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "ee39f9c0-78e5-4aff-9511-ce627e8a7831",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.5751,
  "model_score": 0.5583,
  "style_score": 0.5919,
  "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "87cc4496-aead-4d29-a608-ce349167a8af",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.25,
  "model_score": 0.0,
  "style_score": 0.5,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_MF04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "a7f80f8b-a3f8-4b9d-a237-601ca731b7c3",
  "creator_id": "attacker_MF05",
  "guess": "unsure",
  "confidence": 0.64,
  "model_score": 0.9976,
  "style_score": 0.5,
  "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_MF06",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_MF07",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 413,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 200,
  "content_id": "48b7e469-549e-48a8-8f05-ffffbe8b881c",
  "creator_id": null,
  "guess": "unsure",
  "confidence": 0.3698,
  "model_score": 0.2395,
  "style_score": 0.5,
  "label": "We can't tell whether this was written by a person or by AI. This doesn't mean anything is wrong with your writing. If you wrote it yourself, you can appeal and ask for a person to look at it.",
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 200,
  "content_id": "39543ba4-88a9-43b4-9c0c-8e12dde6fce1",
  "creator_id": {
    "id": "x"
  },
  "guess": "human",
  "confidence": 0.2746,
  "model_score": 0.0492,
  "style_score": 0.5,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "fee43d6b-b4ec-4b71-ab65-f450523ec6f4",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2643,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "dfac3a3f-b936-41e2-b668-111e1016c334",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2643,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "465e8dd6-aaa1-4677-b925-a72075cc2e12",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2643,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "7cebaf55-2703-4f33-9ca4-205c9c34c258",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2643,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "bc60fd3f-654d-4422-bdc9-a25cbec5a646",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.2643,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

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
  "verdict": ""
}
```
