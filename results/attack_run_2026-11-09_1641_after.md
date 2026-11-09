# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-09 16:41
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator*id `attacker*<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID      | Family             | Targeting                                              | Status | Content ID                             | Guess  | Score | Verdict |
| ------- | ------------------ | ------------------------------------------------------ | ------ | -------------------------------------- | ------ | ----- | ------- |
| EV01    | evasion            | signal two: typos raise word variety                   | 200    | `629ba2e6-6b0f-47c6-a523-b0ac25c1427e` | unsure | 0.386 | BROKE   |
| EV02    | evasion            | signal two: broken-up sentences raise length spread    | 200    | `2c677e99-352e-4f28-b7f9-468db8f666a5` | unsure | 0.496 | BROKE   |
| EV03    | evasion            | signal two: a pasted quotation changes the shape       | 200    | `662c9fdb-c374-4c04-9958-73f0f421800f` | unsure | 0.575 | BROKE   |
| EV04    | evasion            | signal one: unusual words raise perplexity             | 200    | `3979d9ce-e4e0-4e1d-8c2b-7f3e262f939a` | unsure | 0.608 | BROKE   |
| EV05    | evasion            | both signals: heavy human editing pass                 | 200    | `b80f763f-403f-4b58-85c1-b6553d9618c9` | unsure | 0.379 | BROKE   |
| EV06    | evasion            | signal two: one very long sentence and one very short  | 200    | `21256e88-87cf-4a57-af35-87b650fb04d1` | unsure | 0.473 | BROKE   |
| EV07    | evasion            | signal two: padding with punctuation                   | 200    | `3c38ada8-0263-4dcf-8ddb-a7872645c427` | unsure | 0.383 | BROKE   |
| EV08    | evasion            | signal one: text below the token window                | 200    | `8c92ca4b-5fb7-4cca-bf3a-6c678780168b` | unsure | 0.409 | BROKE   |
| EV09    | evasion            | both: AI text with a human opening paragraph bolted on | 200    | `0a16b35c-0bc8-43c8-abe6-21f0fc3e5eec` | unsure | 0.603 | BROKE   |
| EV10    | evasion            | signal two: repeated stanza structure                  | 200    | `6b996918-432f-4607-baf4-f8095d430a6d` | ai     | 0.871 | HELD    |
| FP01    | false_positive     | plain, clear human writing with no flourishes          | 200    | `471366ce-610f-42bd-9664-8dac925a0de0` | unsure | 0.602 | HELD    |
| FP02    | false_positive     | human writing in a formal register                     | 200    | `73eb68a6-3016-487f-9666-9572a4fb7820` | unsure | 0.640 | HELD    |
| FP03    | false_positive     | a non-native English speaker writing carefully         | 200    | `81b29057-b595-4ed7-ac13-215cd4fd6a6c` | unsure | 0.640 | HELD    |
| FP04    | false_positive     | a student essay written to a rubric                    | 200    | `81195f8f-f16d-458a-b93f-808d667167be` | unsure | 0.640 | HELD    |
| FP05    | false_positive     | technical documentation written by a person            | 200    | `24985f23-8cf1-45d5-ae8b-68badeb1deb7` | unsure | 0.640 | HELD    |
| FP06    | false_positive     | a person imitating a formal template                   | 200    | `0326df9b-217d-4206-a95d-ca5af24319f2` | unsure | 0.640 | HELD    |
| FP07    | false_positive     | human writing that repeats a phrase deliberately       | 200    | `f99d77eb-8749-49f4-bb20-eb98adee1ac4` | unsure | 0.640 | HELD    |
| FP08    | false_positive     | very short genuine human submission                    | 200    | `9a5a6aa0-c81a-4630-a78b-a2a516314d37` | unsure | 0.422 | HELD    |
| PI01    | prompt_injection   | instruction to ignore the check                        | 200    | `c5a2ed0a-87b0-4014-9c8f-491ea6d69019` | unsure | 0.465 | HELD    |
| PI02    | prompt_injection   | instruction disguised as a system message              | 200    | `4c87822a-8cd6-471d-8794-a2f395556cb7` | human  | 0.305 | HELD    |
| PI03    | prompt_injection   | instruction wrapped in the writer's voice              | 200    | `bec07371-e98e-48a0-94ed-34a015bc262e` | unsure | 0.552 | HELD    |
| PI04    | prompt_injection   | attempt to make the label text hostile                 | 200    | `3842dc88-1030-47df-b876-4ba50388580f` | unsure | 0.488 | HELD    |
| PI05    | prompt_injection   | attempt to inject into the audit log                   | 200    | `b672dcfc-373d-4165-9e4e-8ecad434adfb` | unsure | 0.414 | HELD    |
| PI06    | prompt_injection   | instruction plus real human text                       | 200    | `87277aa1-92b3-4e0a-acd8-cc051c518ed1` | unsure | 0.575 | HELD    |
| MF01    | malformed          | text is only whitespace                                | 400    | `—`                                    | —      | —     | HELD    |
| MF02    | malformed          | text is a single character                             | 422    | `—`                                    | —      | —     | HELD    |
| MF03    | malformed          | text is control characters                             | 200    | `6ee04907-4dd6-4df3-80b9-97b2bef4351e` | human  | 0.250 | HELD    |
| MF04    | malformed          | text is only punctuation                               | 422    | `—`                                    | —      | —     | HELD    |
| MF05    | malformed          | text is a very long single word                        | 200    | `05a50cff-7ae8-49fb-a142-6bcc08e6a6b2` | unsure | 0.640 | HELD    |
| MF06    | malformed          | text is emoji only                                     | 422    | `—`                                    | —      | —     | HELD    |
| MF07    | malformed          | text is right-to-left script                           | 422    | `—`                                    | —      | —     | HELD    |
| MF08    | malformed          | text is 60,000 characters                              | 413    | `—`                                    | —      | —     | HELD    |
| RQ01    | malformed          | no text field at all                                   | 400    | `—`                                    | —      | —     | HELD    |
| RQ02    | malformed          | no creator_id                                          | 200    | `bd095d5d-7741-45ae-9bf7-31eda0af8c42` | unsure | 0.370 | HELD    |
| RQ03    | malformed          | text is a number                                       | 400    | `—`                                    | —      | —     | HELD    |
| RQ04    | malformed          | text is a list                                         | 400    | `—`                                    | —      | —     | HELD    |
| RQ05    | malformed          | text is null                                           | 400    | `—`                                    | —      | —     | HELD    |
| RQ06    | malformed          | creator_id is an object                                | 200    | `a4534fca-61cb-4e69-81cb-22563c2fbc1e` | human  | 0.275 | HELD    |
| RQ07    | malformed          | body is a JSON array, not an object                    | 400    | `—`                                    | —      | —     | HELD    |
| RQ08    | malformed          | body is unparseable JSON                               | 400    | `—`                                    | —      | —     | HELD    |
| RQ09    | malformed          | body is empty                                          | 400    | `—`                                    | —      | —     | HELD    |
| RQ10    | malformed          | body is form-encoded, not JSON                         | 429    | `—`                                    | —      | —     |         |
| RQ11    | malformed          | body is JSON claiming to be plain text                 | 429    | `—`                                    | —      | —     |         |
| RQ12    | malformed          | deeply nested JSON                                     | 400    | `—`                                    | —      | —     | HELD    |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator                  | 200    | `aa022604-5933-4795-9a9d-de312a2b9f9e` | human  | 0.264 | HELD    |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator                  | 200    | `4f61fbe7-8fd0-4ec9-8c6c-b9d41e70cf64` | human  | 0.264 | HELD    |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator                  | 200    | `d7ab123f-5e50-4e53-8c91-8e494ffd4f75` | human  | 0.264 | HELD    |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator                  | 200    | `1f4f291c-383c-4988-ae2e-82281454987a` | human  | 0.264 | HELD    |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator                  | 200    | `134f53f6-31bd-45e0-8f94-fdf57ffde7cc` | human  | 0.264 | HELD    |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator                  | 429    | `—`                                    | —      | —     | HELD    |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator                  | 429    | `—`                                    | —      | —     | HELD    |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator                  | 429    | `—`                                    | —      | —     | HELD    |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator                  | 429    | `—`                                    | —      | —     | HELD    |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator                  | 429    | `—`                                    | —      | —     | HELD    |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator                  | 429    | `—`                                    | —      | —     | HELD    |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator                  | 429    | `—`                                    | —      | —     | HELD    |

---

## By family

| Family               | Attacks | Auto-BROKE | Left to judge |
| -------------------- | ------- | ---------- | ------------- |
| `evasion`            | 10      | 0          | 10            |
| `false_positive`     | 8       | 0          | 8             |
| `flood_same_creator` | 12      | 0          | 12            |
| `malformed`          | 20      | 0          | 20            |
| `prompt_injection`   | 6       | 0          | 6             |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

_Targeting:_ signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "629ba2e6-6b0f-47c6-a523-b0ac25c1427e",
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

_Targeting:_ signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "2c677e99-352e-4f28-b7f9-468db8f666a5",
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

_Targeting:_ signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "662c9fdb-c374-4c04-9958-73f0f421800f",
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

_Targeting:_ signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "3979d9ce-e4e0-4e1d-8c2b-7f3e262f939a",
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

_Targeting:_ both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "b80f763f-403f-4b58-85c1-b6553d9618c9",
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

_Targeting:_ signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "21256e88-87cf-4a57-af35-87b650fb04d1",
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

_Targeting:_ signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "3c38ada8-0263-4dcf-8ddb-a7872645c427",
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

_Targeting:_ signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "8c92ca4b-5fb7-4cca-bf3a-6c678780168b",
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

_Targeting:_ both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "0a16b35c-0bc8-43c8-abe6-21f0fc3e5eec",
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

_Targeting:_ signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "6b996918-432f-4607-baf4-f8095d430a6d",
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

_Targeting:_ plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "471366ce-610f-42bd-9664-8dac925a0de0",
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

_Targeting:_ human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "73eb68a6-3016-487f-9666-9572a4fb7820",
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

_Targeting:_ a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "81b29057-b595-4ed7-ac13-215cd4fd6a6c",
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

_Targeting:_ a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "81195f8f-f16d-458a-b93f-808d667167be",
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

_Targeting:_ technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "24985f23-8cf1-45d5-ae8b-68badeb1deb7",
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

_Targeting:_ a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "0326df9b-217d-4206-a95d-ca5af24319f2",
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

_Targeting:_ human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "f99d77eb-8749-49f4-bb20-eb98adee1ac4",
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

_Targeting:_ very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "9a5a6aa0-c81a-4630-a78b-a2a516314d37",
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

_Targeting:_ instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "c5a2ed0a-87b0-4014-9c8f-491ea6d69019",
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

_Targeting:_ instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "4c87822a-8cd6-471d-8794-a2f395556cb7",
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

_Targeting:_ instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "bec07371-e98e-48a0-94ed-34a015bc262e",
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

_Targeting:_ attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "3842dc88-1030-47df-b876-4ba50388580f",
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

_Targeting:_ attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "b672dcfc-373d-4165-9e4e-8ecad434adfb",
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

_Targeting:_ instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "87277aa1-92b3-4e0a-acd8-cc051c518ed1",
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

_Targeting:_ text is only whitespace

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

_Targeting:_ text is a single character

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

_Targeting:_ text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "6ee04907-4dd6-4df3-80b9-97b2bef4351e",
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

_Targeting:_ text is only punctuation

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

_Targeting:_ text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "05a50cff-7ae8-49fb-a142-6bcc08e6a6b2",
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

_Targeting:_ text is emoji only

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

_Targeting:_ text is right-to-left script

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

_Targeting:_ text is 60,000 characters

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

_Targeting:_ no text field at all

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

_Targeting:_ no creator_id

```json
{
  "id": "RQ02",
  "status": 200,
  "content_id": "bd095d5d-7741-45ae-9bf7-31eda0af8c42",
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

_Targeting:_ text is a number

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

_Targeting:_ text is a list

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

_Targeting:_ text is null

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

_Targeting:_ creator_id is an object

```json
{
  "id": "RQ06",
  "status": 200,
  "content_id": "a4534fca-61cb-4e69-81cb-22563c2fbc1e",
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

_Targeting:_ body is a JSON array, not an object

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

_Targeting:_ body is unparseable JSON

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

_Targeting:_ body is empty

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

_Targeting:_ body is form-encoded, not JSON

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

_Targeting:_ body is JSON claiming to be plain text

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

_Targeting:_ deeply nested JSON

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

_Targeting:_ 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "aa022604-5933-4795-9a9d-de312a2b9f9e",
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

_Targeting:_ 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "4f61fbe7-8fd0-4ec9-8c6c-b9d41e70cf64",
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

_Targeting:_ 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "d7ab123f-5e50-4e53-8c91-8e494ffd4f75",
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

_Targeting:_ 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "1f4f291c-383c-4988-ae2e-82281454987a",
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

_Targeting:_ 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "134f53f6-31bd-45e0-8f94-fdf57ffde7cc",
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

_Targeting:_ 20 rapid submissions from one creator

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

_Targeting:_ 20 rapid submissions from one creator

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

_Targeting:_ 20 rapid submissions from one creator

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

_Targeting:_ 20 rapid submissions from one creator

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

_Targeting:_ 20 rapid submissions from one creator

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

_Targeting:_ 20 rapid submissions from one creator

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
  "verdict": ""
}
```
