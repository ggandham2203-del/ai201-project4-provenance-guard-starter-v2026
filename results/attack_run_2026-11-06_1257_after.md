# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-06 12:57
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

## How I marked

Same rules as the before run (`results/attack_run_2026-11-06_1219_before.md`), applied to the after run. Totals: 42 HELD, 12 BROKE, 2 UNTESTED.

- **FP08** moves from BROKE to HELD: it was refused before and now gets a real decision (human, 0.219).
- **MF04** (punctuation only) and **FL01_01 to FL01_05** went from a 400 to a scored 200 (unsure, 0.5). Under my rule they stay HELD (no crash, no AI accusation), but they are a side effect of the change: junk and flood requests now reach the model instead of being refused cheaply.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `55ed9d1b-a887-4708-9c5b-996ffd840aae` | unsure | 0.385 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `d0929388-e6f8-471e-a8ed-da55e5b0f643` | unsure | 0.500 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `530e870c-81b5-4556-b43d-c41fd38a0827` | unsure | 0.500 | BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `8f4096a1-49c3-4bea-a4c9-26c15a15e485` | unsure | 0.543 | BROKE |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `f608e441-4166-4a9b-a0a4-3bc11c658e87` | human | 0.197 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `ab225f43-f6a1-4934-9ed1-7b49776a1cf3` | human | 0.333 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | `8ba8b782-1ab0-4b0d-808a-ba1a38372295` | unsure | 0.473 | BROKE |
| EV08 | evasion | signal one: text below the token window | 200 | `749456af-0261-42e8-ac5a-26f451c9783b` | human | 0.311 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `a9ecb08d-089d-4202-b814-f8b82941cb61` | unsure | 0.500 | BROKE |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `808ec6cb-6717-4998-aeff-4382dc4982e6` | unsure | 0.500 | BROKE |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `a92ee97b-d436-4ffd-9dbf-e4fdf4884c97` | unsure | 0.500 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `7372513c-3653-4276-b617-9816da29bfc4` | unsure | 0.588 | HELD |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `da59d91d-6e26-4a16-b0ce-f93fb56a21fe` | unsure | 0.500 | HELD |
| FP04 | false_positive | a student essay written to a rubric | 200 | `3fa3bf6f-baa5-4c11-bba3-1f89e0354561` | unsure | 0.500 | HELD |
| FP05 | false_positive | technical documentation written by a person | 200 | `9adc310a-96ab-45f1-ac52-2b7dbb9fe898` | unsure | 0.593 | HELD |
| FP06 | false_positive | a person imitating a formal template | 200 | `99138547-7b9c-4c02-97c2-cb1dbd617cf5` | unsure | 0.500 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `5be78d86-c59b-449b-8f3e-0f211fe7b267` | unsure | 0.500 | HELD |
| FP08 | false_positive | very short genuine human submission | 200 | `0bec8696-b670-43c8-8570-a1a0b00a3969` | human | 0.219 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `2fefa3f7-0cca-4f5e-b316-7557307984b6` | human | 0.275 | BROKE |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `4f7a2d6a-db96-4407-b5ad-a8cf8e17d686` | human | 0.145 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `661e7c8d-aacf-415d-a9a3-b9f87a5d1fa8` | unsure | 0.355 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `cd2b1a39-241e-4dcb-b437-b82c5623b750` | unsure | 0.500 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `ca0e496e-1248-4dad-9c3a-a65bef650dd7` | unsure | 0.500 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `ee50f351-244d-4bdf-87d2-c0f3396764ab` | human | 0.341 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | `—` | — | — | HELD |
| MF03 | malformed | text is control characters | 400 | `—` | — | — | HELD |
| MF04 | malformed | text is only punctuation | 200 | `8dd25e46-756b-4ef3-8780-225e554aa3fc` | unsure | 0.500 | HELD |
| MF05 | malformed | text is a very long single word | 400 | `—` | — | — | HELD |
| MF06 | malformed | text is emoji only | 400 | `—` | — | — | HELD |
| MF07 | malformed | text is right-to-left script | 200 | `4acb95f7-0a65-440d-a0c4-4832c0c1acad` | unsure | 0.500 | HELD |
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
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `9e3de577-ab43-4729-99d9-1531655caedc` | unsure | 0.500 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `8d313ca6-86a3-40ca-805a-3afeb09b11ff` | unsure | 0.500 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `4e1b07a7-4328-4f9d-8366-c0cbcf3cb10a` | unsure | 0.500 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `2a17999b-bd80-4645-bbf0-b6728f11924e` | unsure | 0.500 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `937b22f2-034f-4c66-b2ab-c7644d4a8fa8` | unsure | 0.500 | HELD |
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
  "content_id": "55ed9d1b-a887-4708-9c5b-996ffd840aae",
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
  "content_id": "d0929388-e6f8-471e-a8ed-da55e5b0f643",
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
  "content_id": "530e870c-81b5-4556-b43d-c41fd38a0827",
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
  "content_id": "8f4096a1-49c3-4bea-a4c9-26c15a15e485",
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
  "content_id": "f608e441-4166-4a9b-a0a4-3bc11c658e87",
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
  "content_id": "ab225f43-f6a1-4934-9ed1-7b49776a1cf3",
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
  "content_id": "8ba8b782-1ab0-4b0d-808a-ba1a38372295",
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
  "content_id": "749456af-0261-42e8-ac5a-26f451c9783b",
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
  "content_id": "a9ecb08d-089d-4202-b814-f8b82941cb61",
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
  "content_id": "808ec6cb-6717-4998-aeff-4382dc4982e6",
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
  "content_id": "a92ee97b-d436-4ffd-9dbf-e4fdf4884c97",
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
  "content_id": "7372513c-3653-4276-b617-9816da29bfc4",
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
  "content_id": "da59d91d-6e26-4a16-b0ce-f93fb56a21fe",
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
  "content_id": "3fa3bf6f-baa5-4c11-bba3-1f89e0354561",
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
  "content_id": "9adc310a-96ab-45f1-ac52-2b7dbb9fe898",
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
  "content_id": "99138547-7b9c-4c02-97c2-cb1dbd617cf5",
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
  "content_id": "5be78d86-c59b-449b-8f3e-0f211fe7b267",
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
  "status": 200,
  "content_id": "0bec8696-b670-43c8-8570-a1a0b00a3969",
  "creator_id": "attacker_FP08",
  "guess": "human",
  "confidence": 0.2189,
  "model_score": 0.3223,
  "style_score": 0.15,
  "label": "This looks like it was written by a person.",
  "error": null,
  "verdict": "HELD"
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "2fefa3f7-0cca-4f5e-b316-7557307984b6",
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
  "content_id": "4f7a2d6a-db96-4407-b5ad-a8cf8e17d686",
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
  "content_id": "661e7c8d-aacf-415d-a9a3-b9f87a5d1fa8",
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
  "content_id": "cd2b1a39-241e-4dcb-b437-b82c5623b750",
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
  "content_id": "ca0e496e-1248-4dad-9c3a-a65bef650dd7",
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
  "content_id": "ee50f351-244d-4bdf-87d2-c0f3396764ab",
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
  "status": 200,
  "content_id": "8dd25e46-756b-4ef3-8780-225e554aa3fc",
  "creator_id": "attacker_MF04",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0112,
  "style_score": 0.5,
  "label": "We can't tell for sure whether this was written by a person or with an AI tool. This isn't a finding that anything is wrong. If you'd like someone to take a look, you can send us a note.",
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
  "content_id": "4acb95f7-0a65-440d-a0c4-4832c0c1acad",
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
  "status": 200,
  "content_id": "9e3de577-ab43-4729-99d9-1531655caedc",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We can't tell for sure whether this was written by a person or with an AI tool. This isn't a finding that anything is wrong. If you'd like someone to take a look, you can send us a note.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "8d313ca6-86a3-40ca-805a-3afeb09b11ff",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We can't tell for sure whether this was written by a person or with an AI tool. This isn't a finding that anything is wrong. If you'd like someone to take a look, you can send us a note.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "4e1b07a7-4328-4f9d-8366-c0cbcf3cb10a",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We can't tell for sure whether this was written by a person or with an AI tool. This isn't a finding that anything is wrong. If you'd like someone to take a look, you can send us a note.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "2a17999b-bd80-4645-bbf0-b6728f11924e",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We can't tell for sure whether this was written by a person or with an AI tool. This isn't a finding that anything is wrong. If you'd like someone to take a look, you can send us a note.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "937b22f2-034f-4c66-b2ab-c7644d4a8fa8",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "We can't tell for sure whether this was written by a person or with an AI tool. This isn't a finding that anything is wrong. If you'd like someone to take a look, you can send us a note.",
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
