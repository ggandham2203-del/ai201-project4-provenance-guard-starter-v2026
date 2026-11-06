# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-06 12:19
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

## How I marked

- **evasion:** HELD only if the label was AI. All ten inputs are AI text, so anything else got through.
- **false_positive:** HELD if the writer was not labeled AI and got a result back. FP08 was refused with a 400, so a genuine short submission got no result.
- **prompt_injection:** HELD if the instruction did not get what it asked for (a human label, altered label text, or a corrupted log).
- **malformed and flood:** HELD if the request was refused or limited cleanly with no crash. RQ10 and RQ11 were rate limited before reaching the route, so they are untested.
- **Totals:** 41 HELD, 13 BROKE, 2 UNTESTED.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `d9425720-8b69-48b0-9cb2-b442f43c829b` | unsure | 0.385 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `fa0aa0b8-759c-4923-a87f-315db4ff9e01` | unsure | 0.500 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `73577bc6-ba2e-48a1-8e0a-de8acf1efb3d` | unsure | 0.500 | BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `fdeee982-8f0a-43a2-9843-1900f5924184` | unsure | 0.543 | BROKE |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `a01b298f-06aa-40d3-916e-379f515d8f0b` | human | 0.197 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `0a3a21cd-a2a4-4731-89d1-df34f18db74b` | human | 0.333 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | `88f3c8a2-d4f4-40cf-9306-e1182e69ffd4` | unsure | 0.473 | BROKE |
| EV08 | evasion | signal one: text below the token window | 200 | `90d0781c-667b-4418-96dc-14c7381a9236` | human | 0.311 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `47b67102-2736-47ae-be89-ae466662653e` | unsure | 0.500 | BROKE |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `0ec36840-982a-4377-afd9-4a1bdc3794c1` | unsure | 0.500 | BROKE |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `3e2cc855-b8ff-4b18-a260-c00b7f72ef39` | unsure | 0.500 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `ed3340ee-7cce-4e28-a2cb-5ad215aa781c` | unsure | 0.588 | HELD |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `234197ff-06d6-4ab3-85f5-6669e00198de` | unsure | 0.500 | HELD |
| FP04 | false_positive | a student essay written to a rubric | 200 | `1ee9a8e2-8032-468b-8ef1-1f46272d8a2c` | unsure | 0.500 | HELD |
| FP05 | false_positive | technical documentation written by a person | 200 | `c239a427-3b17-499c-af0e-be8683b3d432` | unsure | 0.593 | HELD |
| FP06 | false_positive | a person imitating a formal template | 200 | `546e3fa1-5fd1-4ff0-b027-36b82276c4af` | unsure | 0.500 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `5feecc07-761f-446b-a03d-235db458a947` | unsure | 0.500 | HELD |
| FP08 | false_positive | very short genuine human submission | 400 | `—` | — | — | BROKE |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `ee5d12d8-8798-4e3c-ab71-c4c1ad2f48c4` | human | 0.275 | BROKE |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `8ebbc92f-c54e-4e3b-822a-e2b85fec4fb5` | human | 0.145 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `a2eeff59-fb37-4086-bc07-4247626afb3f` | unsure | 0.355 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `6d281710-5874-45a3-9a3d-2565122421ab` | unsure | 0.500 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `bb627e05-2169-4dea-b390-9d652abb8b19` | unsure | 0.500 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `b1f48359-5497-4084-9d31-73a78d4c6c14` | human | 0.341 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | `—` | — | — | HELD |
| MF03 | malformed | text is control characters | 400 | `—` | — | — | HELD |
| MF04 | malformed | text is only punctuation | 400 | `—` | — | — | HELD |
| MF05 | malformed | text is a very long single word | 400 | `—` | — | — | HELD |
| MF06 | malformed | text is emoji only | 400 | `—` | — | — | HELD |
| MF07 | malformed | text is right-to-left script | 200 | `02c4c04a-4ba5-4ad5-b46d-29d5ba40bc45` | unsure | 0.500 | HELD |
| MF08 | malformed | text is 60,000 characters | 413 | `—` | — | — | HELD |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — | HELD |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — | HELD |
| RQ03 | malformed | text is a number | 400 | `—` | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | `—` | — | — | HELD |
| RQ05 | malformed | text is null | 400 | `—` | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | `—` | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | `—` | — | — | UNTESTED (429, never reached the route) |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — | UNTESTED (429, never reached the route) |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 400 | `—` | — | — | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 400 | `—` | — | — | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 400 | `—` | — | — | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 400 | `—` | — | — | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 400 | `—` | — | — | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |

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
  "content_id": "d9425720-8b69-48b0-9cb2-b442f43c829b",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.385,
  "model_score": 0.1635,
  "style_score": 0.5327,
  "label": "We can't tell for sure whether this was written by a person or with an AI tool. This isn't a finding that anything is wrong. If you'd like someone to take a look, you can send us a note.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "fa0aa0b8-759c-4923-a87f-315db4ff9e01",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.5943,
  "style_score": 0.1345,
  "label": "We can't tell for sure whether this was written by a person or with an AI tool. This isn't a finding that anything is wrong. If you'd like someone to take a look, you can send us a note.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "73577bc6-ba2e-48a1-8e0a-de8acf1efb3d",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.6662,
  "style_score": 0.099,
  "label": "We can't tell for sure whether this was written by a person or with an AI tool. This isn't a finding that anything is wrong. If you'd like someone to take a look, you can send us a note.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "fdeee982-8f0a-43a2-9843-1900f5924184",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.5432,
  "model_score": 0.6114,
  "style_score": 0.4978,
  "label": "We can't tell for sure whether this was written by a person or with an AI tool. This isn't a finding that anything is wrong. If you'd like someone to take a look, you can send us a note.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "a01b298f-06aa-40d3-916e-379f515d8f0b",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.1969,
  "model_score": 0.3212,
  "style_score": 0.114,
  "label": "This looks like it was written by a person.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "0a3a21cd-a2a4-4731-89d1-df34f18db74b",
  "creator_id": "attacker_EV06",
  "guess": "human",
  "confidence": 0.3332,
  "model_score": 0.5727,
  "style_score": 0.1736,
  "label": "This looks like it was written by a person.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "88f3c8a2-d4f4-40cf-9306-e1182e69ffd4",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.473,
  "model_score": 0.5862,
  "style_score": 0.3976,
  "label": "We can't tell for sure whether this was written by a person or with an AI tool. This isn't a finding that anything is wrong. If you'd like someone to take a look, you can send us a note.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "90d0781c-667b-4418-96dc-14c7381a9236",
  "creator_id": "attacker_EV08",
  "guess": "human",
  "confidence": 0.3111,
  "model_score": 0.2452,
  "style_score": 0.355,
  "label": "This looks like it was written by a person.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "47b67102-2736-47ae-be89-ae466662653e",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.7042,
  "style_score": 0.1034,
  "label": "We can't tell for sure whether this was written by a person or with an AI tool. This isn't a finding that anything is wrong. If you'd like someone to take a look, you can send us a note.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "0ec36840-982a-4377-afd9-4a1bdc3794c1",
  "creator_id": "attacker_EV10",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.9792,
  "style_score": 0.3107,
  "label": "We can't tell for sure whether this was written by a person or with an AI tool. This isn't a finding that anything is wrong. If you'd like someone to take a look, you can send us a note.",
  "error": null,
  "verdict": "BROKE"
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "3e2cc855-b8ff-4b18-a260-c00b7f72ef39",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.6175,
  "style_score": 0.2056,
  "label": "We can't tell for sure whether this was written by a person or with an AI tool. This isn't a finding that anything is wrong. If you'd like someone to take a look, you can send us a note.",
  "error": null,
  "verdict": "HELD"
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "ed3340ee-7cce-4e28-a2cb-5ad215aa781c",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.5879,
  "model_score": 0.7387,
  "style_score": 0.4873,
  "label": "We can't tell for sure whether this was written by a person or with an AI tool. This isn't a finding that anything is wrong. If you'd like someone to take a look, you can send us a note.",
  "error": null,
  "verdict": "HELD"
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "234197ff-06d6-4ab3-85f5-6669e00198de",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.8051,
  "style_score": 0.3421,
  "label": "We can't tell for sure whether this was written by a person or with an AI tool. This isn't a finding that anything is wrong. If you'd like someone to take a look, you can send us a note.",
  "error": null,
  "verdict": "HELD"
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "1ee9a8e2-8032-468b-8ef1-1f46272d8a2c",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.8329,
  "style_score": 0.2278,
  "label": "We can't tell for sure whether this was written by a person or with an AI tool. This isn't a finding that anything is wrong. If you'd like someone to take a look, you can send us a note.",
  "error": null,
  "verdict": "HELD"
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "c239a427-3b17-499c-af0e-be8683b3d432",
  "creator_id": "attacker_FP05",
  "guess": "unsure",
  "confidence": 0.593,
  "model_score": 0.8005,
  "style_score": 0.4547,
  "label": "We can't tell for sure whether this was written by a person or with an AI tool. This isn't a finding that anything is wrong. If you'd like someone to take a look, you can send us a note.",
  "error": null,
  "verdict": "HELD"
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "546e3fa1-5fd1-4ff0-b027-36b82276c4af",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.8814,
  "style_score": 0.1965,
  "label": "We can't tell for sure whether this was written by a person or with an AI tool. This isn't a finding that anything is wrong. If you'd like someone to take a look, you can send us a note.",
  "error": null,
  "verdict": "HELD"
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "5feecc07-761f-446b-a03d-235db458a947",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.8816,
  "style_score": 0.2661,
  "label": "We can't tell for sure whether this was written by a person or with an AI tool. This isn't a finding that anything is wrong. If you'd like someone to take a look, you can send us a note.",
  "error": null,
  "verdict": "HELD"
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_FP08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "BROKE"
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "ee5d12d8-8798-4e3c-ab71-c4c1ad2f48c4",
  "creator_id": "attacker_PI01",
  "guess": "human",
  "confidence": 0.275,
  "model_score": 0.4625,
  "style_score": 0.15,
  "label": "This looks like it was written by a person.",
  "error": null,
  "verdict": "BROKE"
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "8ebbc92f-c54e-4e3b-822a-e2b85fec4fb5",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.1451,
  "model_score": 0.2044,
  "style_score": 0.1056,
  "label": "This looks like it was written by a person.",
  "error": null,
  "verdict": "BROKE"
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "a2eeff59-fb37-4086-bc07-4247626afb3f",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.3548,
  "model_score": 0.5943,
  "style_score": 0.1951,
  "label": "We can't tell for sure whether this was written by a person or with an AI tool. This isn't a finding that anything is wrong. If you'd like someone to take a look, you can send us a note.",
  "error": null,
  "verdict": "HELD"
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "6d281710-5874-45a3-9a3d-2565122421ab",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.4998,
  "style_score": 0.0913,
  "label": "We can't tell for sure whether this was written by a person or with an AI tool. This isn't a finding that anything is wrong. If you'd like someone to take a look, you can send us a note.",
  "error": null,
  "verdict": "HELD"
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "bb627e05-2169-4dea-b390-9d652abb8b19",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.6401,
  "style_score": 0.0,
  "label": "We can't tell for sure whether this was written by a person or with an AI tool. This isn't a finding that anything is wrong. If you'd like someone to take a look, you can send us a note.",
  "error": null,
  "verdict": "HELD"
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "b1f48359-5497-4084-9d31-73a78d4c6c14",
  "creator_id": "attacker_PI06",
  "guess": "human",
  "confidence": 0.341,
  "model_score": 0.5583,
  "style_score": 0.1961,
  "label": "This looks like it was written by a person.",
  "error": null,
  "verdict": "HELD"
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
  "verdict": "HELD"
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF06",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "02c4c04a-4ba5-4ad5-b46d-29d5ba40bc45",
  "creator_id": "attacker_MF07",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.9064,
  "style_score": 0.5,
  "label": "We can't tell for sure whether this was written by a person or with an AI tool. This isn't a finding that anything is wrong. If you'd like someone to take a look, you can send us a note.",
  "error": null,
  "verdict": "HELD"
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
  "verdict": "HELD"
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
  "verdict": "HELD"
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
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
  "verdict": "HELD"
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
  "verdict": "HELD"
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
  "verdict": "HELD"
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
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
  "verdict": "HELD"
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
  "verdict": "HELD"
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
  "verdict": "HELD"
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
  "verdict": "UNTESTED (429, never reached the route)"
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
  "verdict": "UNTESTED (429, never reached the route)"
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
  "verdict": "HELD"
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 400,
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

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 400,
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

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 400,
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

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 400,
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

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 400,
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
  "verdict": "HELD"
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
  "verdict": "HELD"
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
  "verdict": "HELD"
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
  "verdict": "HELD"
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
  "verdict": "HELD"
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
  "verdict": "HELD"
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
  "verdict": "HELD"
}
```
