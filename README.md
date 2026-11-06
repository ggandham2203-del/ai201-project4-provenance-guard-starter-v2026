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

Provenance Guard is a small backend service a writing site could plug into. A writer's text goes in; a guess, a confidence number, a plain-English label and a way to appeal come out. It is built so that when it isn't sure, it says so instead of accusing someone.

The path a submission takes:

1. **`POST /submit`** (`app.py::submit`) receives `{text, creator_id}`. It rejects bad input (400 for a missing or empty field or text under 10 words, 413 for text over 10,000 characters), logs the rejection, and makes a `content_id` (a uuid).
2. **`detector.py::model_signal`** runs GPT-2 on the text and returns `model_score`, 0 to 1. Higher means more likely AI.
3. **`stylometry.py::style_signal`** measures the shape of the text and returns `style_score`, 0 to 1. Higher means more likely AI.
4. **`scoring.py::combine_signals`** merges the two into one combined score, which is the `confidence`.
5. **`scoring.py::score_to_label`** turns that number into a `guess` (`ai`, `human` or `unsure`) and the sentence the writer reads.
6. **`audit.py::log_decision`** appends the decision (all three scores, the label, status `decided`) to `logs/audit.jsonl`.
7. **`/submit`** returns JSON with `content_id`, `guess`, `confidence`, `label`, `model_score` and `style_score`.

If a writer disagrees, **`POST /appeal`** (`app.py::appeal`) takes the `content_id` and their reasoning, checks the id exists (404 and nothing logged if it doesn't), appends an appeal entry with status `under_review` next to the original decision, and confirms. The log is append-only, so the original decision is never overwritten.

---

## Signals and Scoring

### Signal one — the model signal

**What it measures:** how predictable the text is to a language model (GPT-2 running locally). It computes perplexity and squashes it to 0 to 1, where low perplexity (predictable text) gives a high AI score. Code: `detector.py::model_signal`.

**Why that might differ between human and AI writing:** an AI writes by picking likely next words, so its text tends to be easy for a model to predict. Human writing wanders more, with odd word choices and specific details.

**What it can't see:** authorship. Predictability is not the same as who wrote something. It rewards common words in short, ordinary sentences, so plain human writing scores as AI-like. In my own tests, two plain paragraphs I wrote scored 0.71 and 0.81, and my formal, plain-worded report paragraph scored 0.71. Meanwhile an AI sentence full of unusual wording scored 0.05, and an AI weather paragraph full of numbers and symbols scored 0.42. It is also easy to move: adding three typos to an AI paragraph dropped its model score from 0.885 to 0.639, because misspelled words surprise the model.

### Signal two — the style signal

**What it measures:** the shape of the text, without reading it. Three measures in `stylometry.py`: sentence-length spread (standard deviation divided by mean sentence length), word variety (unique words over total words, over the first 100 words), and punctuation density (commas, semicolons, colons, dashes, parentheses and quotes per word). `style_signal` flips each so higher means more likely AI and blends them.

**Why that might differ between human and AI writing:** AI prose tends toward even, mid-length sentences and a narrower vocabulary. Human writing is lumpier, with a short sentence next to a long one.

**What it can't see:** meaning. It has no idea what the text says, so anything that changes the shape without changing the substance moves it. A text of one sentence has no spread at all, so I made that case neutral (0.5) instead of treating it as AI-like. In my tests only sentence spread really separated the groups: the three AI paragraphs had spread 0.14 to 0.16 and the three human paragraphs 0.30 to 0.40. Word variety and punctuation mostly added noise. For example, the AI weather paragraph has many commas and a wide vocabulary, so both measures read it as human. Splitting sentences or pasting in a quotation would move this signal cheaply.

### The combining rule

**The rule:** two steps. First, if the two signals disagree by more than 0.4, the system doesn't actually know, so the combined score is forced to 0.5, which is the middle of the unsure band. Second, otherwise a weighted average where the style signal counts more than the model signal, because the model signal was the one that accused plain human writing in my tests. Inside the style signal, spread carries most of the weight for the same reason: it was the only measure that separated my test texts.

**The numbers:**
- Combined score: 0.4 x model score + 0.6 x style score (`config.py`: `WEIGHT_MODEL_SIGNAL`, `WEIGHT_STYLE_SIGNAL`)
- Disagreement gap: 0.4 (`config.py`: `DISAGREEMENT_GAP`)
- Inside the style signal: 0.7 spread, 0.15 word variety, 0.15 punctuation. Spread counts as fully human at 0.4 or above (`stylometry.py` constants)
- Thresholds: human below 0.35, AI above 0.65 (`config.py`: `HUMAN_THRESHOLD`, `AI_THRESHOLD`), unchanged from the starter

**Where it lives:** `scoring.py::combine_signals`

**A case where my two signals split, and what my rule does with it:** my formal report paragraph (written by me). Signal one scored it 0.706 (AI-like, because the wording is plain and common) while signal two scored it 0.181 (very human-like, because the sentence lengths vary a lot). The gap is 0.53, so the rule forces the combined score to 0.50 and the label is unsure, not an accusation. Without the rule it would have been 0.39, also unsure, so here the rule agreed with the plain average. Another split, from the live service: my remote-work paragraph scored 0.536 on the model signal and 0.075 on style (a gap of 0.46), so the rule returned 0.5 and the label was unsure.

**Honest limits.** I tuned the weights on the same ten texts I am describing, so these numbers are probably better than they would be on new text. On those ten texts the combined average was about 0.51 for AI text and 0.44 for my own, so the signals together barely separate the two groups, and my criterion 2 (a gap of at least 0.3) would fail. Lightly editing an AI paragraph (three typos) took it from 0.691 (AI) to 0.573 (unsure), so that kind of evasion works. I accepted that trade on purpose: a wide unsure band means fewer wrong accusations, and the cost is that some AI text gets through as unsure.

---

## Label Variants

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 - 0.35 | This looks like it was written by a person. |
| unsure | 0.35 - 0.65 | We can't tell for sure whether this was written by a person or with an AI tool. This isn't a finding that anything is wrong. If you'd like someone to take a look, you can send us a note. |
| high-confidence AI | 0.65 - 1.00 | This may have been written with an AI tool. We can get this wrong, especially with plain or simple writing. If you wrote it yourself, tell us and a person will review it. |

The boundaries are inclusive: exactly 0.35 gets the human label and exactly 0.65 gets the AI label.

**Why I worded the "unsure" one this way:** the person reading it may have written every word themselves, so it says plainly that we can't tell and that this is not a finding that anything is wrong. It also gives them a way to ask for a second look. The AI label hedges as well ("may have been", "we can get this wrong") and points at the appeal, because the person who gets it is the false positive this project is built around.

---

## Sample Run

**A submission**

```bash
$ curl -X POST http://127.0.0.1:5000/submit -H "Content-Type: application/json" -d @- <<'EOF'
{"text": "The Big Bang Theory is the scientific explanation for how the universe began about 13.8 billion years ago. The universe started in an extremely hot and dense state and has been expanding and cooling ever since. Over time, stars, galaxies, and planets formed as matter came together under gravity. Scientists support this theory through evidence such as the expansion of the universe and cosmic microwave background radiation.", "creator_id": "me"}
EOF
```

```json
{
  "confidence": 0.691,
  "content_id": "5a0dc67e-c4e6-4ed1-851e-5e24ad169c8f",
  "guess": "ai",
  "label": "This may have been written with an AI tool. We can get this wrong, especially with plain or simple writing. If you wrote it yourself, tell us and a person will review it.",
  "model_score": 0.8855,
  "style_score": 0.5613
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal -H "Content-Type: application/json" \
  -d '{"content_id": "5a0dc67e-c4e6-4ed1-851e-5e24ad169c8f", "reasoning": "I wrote this myself for a physics class."}'
```

```json
{
  "content_id": "5a0dc67e-c4e6-4ed1-851e-5e24ad169c8f",
  "message": "Thanks. Your appeal has been recorded and a person will review it.",
  "status": "under_review"
}
```

**What the log shows afterwards**

The two entries for this content id from `logs/audit.jsonl`: the original decision, then the appeal after it.

```json
{"timestamp": "2026-10-29T02:44:49+00:00", "content_id": "5a0dc67e-c4e6-4ed1-851e-5e24ad169c8f", "creator_id": "me", "guess": "ai", "model_score": 0.8855, "style_score": 0.5613, "combined_score": 0.691, "label": "This may have been written with an AI tool. We can get this wrong, especially with plain or simple writing. If you wrote it yourself, tell us and a person will review it.", "status": "decided"}
{"timestamp": "2026-10-29T02:46:11+00:00", "content_id": "5a0dc67e-c4e6-4ed1-851e-5e24ad169c8f", "creator_id": "me", "event": "appeal", "status": "under_review", "reasoning": "I wrote this myself for a physics class."}
```

An appeal with an id that doesn't exist returns a 404 and writes nothing to the log.

---

## How I Used AI

**Moment 1: the style signal**

- *What I asked for:* the second signal in `stylometry.py`, then a combining rule that fit what my tests showed.
- *What came back:* a first version of the three measures. When I ran six texts through it, it scored my own plain writing as more AI-like than the AI paragraph. Claude traced one cause to a bug (a one-sentence text counted as maximally AI-like) and I approved the fix. After I added four paragraphs, Claude tried three weightings on all ten texts, found that only sentence spread separated them, and proposed weighting spread heavily, weighting style over the model signal, and forcing disagreements to unsure.
- *What I changed:* I supplied and ran all the test texts on my own machine, chose which of the proposed weightings and rules to accept, and approved each edit before it went in. I kept the thresholds unchanged instead of tuning them to rescue individual results.

**Moment 2: reading my labels as the writer**

- *What I asked for:* how a writer would read each of my three labels, answered as the writer, without rewriting them.
- *What came back:* the "unsure" label's reassurance ("this isn't a finding that anything is wrong") could backfire and make a writer wonder what is wrong. The "unsure" and "AI" labels both hedge, so a reader may not feel much difference between them. And both tell the writer to act ("send us a note", "tell us") without saying how.
- *What I changed:* nothing yet, but I noted that the site needs a visible way to appeal.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 5 per minute, 50 per day (`config.py`: `RATE_LIMIT_PER_MINUTE`, `RATE_LIMIT_PER_DAY`), applied to `POST /submit`.

**Why those numbers and not others:** a real writer revising one piece might submit it ten times in a sitting, but is very unlikely to send five in the same minute, and 50 in a day is far more than anyone submitting their own work needs. A script trying to map my thresholds needs hundreds of probes, so 50 a day shuts that down. The starter's default was 10 per minute and 200 per day, which would let a script run 200 probes a day from one caller.

**What a caller counts as:** the `creator_id` in the request body, falling back to the network address when there is no usable one (`app.py::rate_limit_key`). That fails in a specific way: a script that sends every request under a new `creator_id` never trips the limit, and every row of the attack set except the flood family does exactly that. A request with no usable `creator_id` counts against my own address instead, which is why two malformed attack rows (RQ10, RQ11) came back 429 without ever reaching my route.

**The run of status codes when I pushed past it:**

```
$ python run_attacks.py --flood 15
200 200 200 200 200 429 429 429 429 429 429 429 429 429 429
```

Ten of fifteen were rate limited, and every rejection is in the audit log (`"reason": "rate_limited"`, `"limit": "5 per 1 minute"`).

---

## Attack Run — Before

56 attacks, run before changing anything (`python run_attacks.py --set attack_set --label before`, full output in `results/attack_run_2026-11-06_1219_before.md`). Nothing crashed and nothing returned a 5xx.

**How I marked:** evasion is HELD only if the label was AI (all ten inputs are AI text, so anything else got through). A false-positive input is HELD if the writer was not labeled AI and got a result back. A prompt injection is HELD if the instruction did not get what it asked for (a human label, altered label text, or a corrupted log). Malformed and flood inputs are HELD if the request was refused or limited cleanly with no crash.

**Totals: 41 HELD, 13 BROKE, 2 UNTESTED.** None of the 56 attacks was labeled AI.

| Family | Attacks | HELD | BROKE | UNTESTED |
|---|---|---|---|---|
| evasion | 10 | 0 | 10 | 0 |
| false_positive | 8 | 7 | 1 | 0 |
| prompt_injection | 6 | 4 | 2 | 0 |
| malformed | 20 | 18 | 0 | 2 |
| flood_same_creator | 12 | 12 | 0 | 0 |

| ID | Family | Targeting | Status | Result | Mark |
|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | unsure 0.385 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | unsure 0.500 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | unsure 0.500 | BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | unsure 0.543 | BROKE |
| EV05 | evasion | both signals: heavy human editing pass | 200 | human 0.197 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | human 0.333 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | unsure 0.473 | BROKE |
| EV08 | evasion | signal one: text below the token window | 200 | human 0.311 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | unsure 0.500 | BROKE |
| EV10 | evasion | signal two: repeated stanza structure | 200 | unsure 0.500 | BROKE |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | unsure 0.500 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | unsure 0.588 | HELD |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | unsure 0.500 | HELD |
| FP04 | false_positive | a student essay written to a rubric | 200 | unsure 0.500 | HELD |
| FP05 | false_positive | technical documentation written by a person | 200 | unsure 0.593 | HELD |
| FP06 | false_positive | a person imitating a formal template | 200 | unsure 0.500 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | unsure 0.500 | HELD |
| FP08 | false_positive | very short genuine human submission | 400 | refused | BROKE |
| PI01 | prompt_injection | instruction to ignore the check | 200 | human 0.275 | BROKE |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | human 0.145 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | unsure 0.355 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | unsure 0.500 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | unsure 0.500 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | human 0.341 | HELD |
| MF01 | malformed | text is only whitespace | 400 | refused | HELD |
| MF02 | malformed | text is a single character | 400 | refused | HELD |
| MF03 | malformed | text is control characters | 400 | refused | HELD |
| MF04 | malformed | text is only punctuation | 400 | refused | HELD |
| MF05 | malformed | text is a very long single word | 400 | refused | HELD |
| MF06 | malformed | text is emoji only | 400 | refused | HELD |
| MF07 | malformed | text is right-to-left script | 200 | unsure 0.500 | HELD |
| MF08 | malformed | text is 60,000 characters | 413 | refused | HELD |
| RQ01 | malformed | no text field at all | 400 | refused | HELD |
| RQ02 | malformed | no creator_id | 400 | refused | HELD |
| RQ03 | malformed | text is a number | 400 | refused | HELD |
| RQ04 | malformed | text is a list | 400 | refused | HELD |
| RQ05 | malformed | text is null | 400 | refused | HELD |
| RQ06 | malformed | creator_id is an object | 400 | refused | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | refused | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | refused | HELD |
| RQ09 | malformed | body is empty | 400 | refused | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | rate limited | UNTESTED (429, never reached the route) |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | rate limited | UNTESTED (429, never reached the route) |
| RQ12 | malformed | deeply nested JSON | 400 | refused | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 400 | refused | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 400 | refused | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 400 | refused | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 400 | refused | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 400 | refused | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | rate limited | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | rate limited | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | rate limited | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | rate limited | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | rate limited | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | rate limited | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | rate limited | HELD |

RQ10 and RQ11 were rate limited before they reached my route, so what the route does with them is untested.

**Ten audit log entries from the run**

Seven decisions and three rejections, chosen to show the interesting failures. A rejection carries fewer fields than a decision: no content id and no scores.

```json
{"timestamp": "2026-11-06T18:19:13+00:00", "content_id": "a01b298f-06aa-40d3-916e-379f515d8f0b", "creator_id": "attacker_EV05", "guess": "human", "model_score": 0.3212, "style_score": 0.114, "combined_score": 0.1969, "label": "This looks like it was written by a person.", "status": "decided"}
{"timestamp": "2026-11-06T18:19:13+00:00", "content_id": "0ec36840-982a-4377-afd9-4a1bdc3794c1", "creator_id": "attacker_EV10", "guess": "unsure", "model_score": 0.9792, "style_score": 0.3107, "combined_score": 0.5, "label": "We can't tell for sure whether this was written by a person or with an AI tool. This isn't a finding that anything is wrong. If you'd like someone to take a look, you can send us a note.", "status": "decided"}
{"timestamp": "2026-11-06T18:19:13+00:00", "content_id": "fa0aa0b8-759c-4923-a87f-315db4ff9e01", "creator_id": "attacker_EV02", "guess": "unsure", "model_score": 0.5943, "style_score": 0.1345, "combined_score": 0.5, "label": "We can't tell for sure whether this was written by a person or with an AI tool. This isn't a finding that anything is wrong. If you'd like someone to take a look, you can send us a note.", "status": "decided"}
{"timestamp": "2026-11-06T18:19:14+00:00", "content_id": "ed3340ee-7cce-4e28-a2cb-5ad215aa781c", "creator_id": "attacker_FP02", "guess": "unsure", "model_score": 0.7387, "style_score": 0.4873, "combined_score": 0.5879, "label": "We can't tell for sure whether this was written by a person or with an AI tool. This isn't a finding that anything is wrong. If you'd like someone to take a look, you can send us a note.", "status": "decided"}
{"timestamp": "2026-11-06T18:19:14+00:00", "content_id": "c239a427-3b17-499c-af0e-be8683b3d432", "creator_id": "attacker_FP05", "guess": "unsure", "model_score": 0.8005, "style_score": 0.4547, "combined_score": 0.593, "label": "We can't tell for sure whether this was written by a person or with an AI tool. This isn't a finding that anything is wrong. If you'd like someone to take a look, you can send us a note.", "status": "decided"}
{"timestamp": "2026-11-06T18:19:14+00:00", "content_id": "ee5d12d8-8798-4e3c-ab71-c4c1ad2f48c4", "creator_id": "attacker_PI01", "guess": "human", "model_score": 0.4625, "style_score": 0.15, "combined_score": 0.275, "label": "This looks like it was written by a person.", "status": "decided"}
{"timestamp": "2026-11-06T18:19:14+00:00", "content_id": "bb627e05-2169-4dea-b390-9d652abb8b19", "creator_id": "attacker_PI05", "guess": "unsure", "model_score": 0.6401, "style_score": 0.0, "combined_score": 0.5, "label": "We can't tell for sure whether this was written by a person or with an AI tool. This isn't a finding that anything is wrong. If you'd like someone to take a look, you can send us a note.", "status": "decided"}
{"timestamp": "2026-11-06T18:19:14+00:00", "creator_id": "attacker_FP08", "event": "rejected", "status": "rejected", "reason": "text_too_short"}
{"timestamp": "2026-11-06T18:19:14+00:00", "creator_id": "attacker_flood", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "5 per 1 minute"}
{"timestamp": "2026-11-06T18:19:14+00:00", "creator_id": "attacker_MF08", "event": "rejected", "status": "rejected", "reason": "text_too_long"}
```

**The single worst outcome** — FP08, the genuine short submission:

> Went for a run. Legs hurt. Worth it.

My service answered with a 400 (`text_too_short`) and no result. That is eight words, and my route refuses anything under ten. A real writer who posted a short piece of their own work got an error instead of a decision. Because no decision was made, there is no `content_id`, so they have nothing to appeal with either. Of everything in the run, this is the one I would least want to explain: the system did not misjudge their writing, it refused to look at it, and it left them no way to push back.

---

## Run Log and Verdicts

Five criteria, three trials each, nothing changed in between (`python run_eval.py --label before`, full output in `results/run_2026-11-06_1239_before.md`; the appeal test in `results/appeal_check_before.txt`). The scenarios are in `scenarios.py`. Every text scored identically on all three trials, so the repeats show a stable result rather than a lucky one.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. My own writing labeled AI | 0 of 10 | 0/10 | 0/10 | 0/10 | MET |
| 2. AI average above human average | at least 0.3 | +0.236 | +0.236 | +0.236 | **MISSED** |
| 3. All three labels reachable | 3 of 3 | 3/3 | 3/3 | 3/3 | MET |
| 4. Gap over 0.4 means unsure | no exceptions | 0 exceptions | 0 exceptions | 0 exceptions | MET |
| 5. Appeals always work | 100% | 5/5 | 5/5 | 5/5 | MET |

**How I decided each verdict**

1. None of my ten texts was labeled AI on any trial. But only three got the human label and seven got "unsure", so the unsure band is absorbing my writing rather than the system recognizing it. Five of the ten (dejected, too many things, K-Pop, project report, formal report) were also the texts I tuned the weights on in unit 7, so only the other five are fresh.
2. The AI paragraphs averaged 0.622 and the human paragraphs 0.386, a gap of 0.236 against a target of 0.3. A miss on every trial. I did not change the target.
3. The three texts produced `ai` (0.691), `unsure` (0.5) and `human` (0.338) on every trial.
4. 21 of the 81 results had a model/style gap over 0.4 and all 21 were labeled unsure. This is close to guaranteed by construction: `scoring.py::combine_signals` returns exactly 0.5 whenever the gap exceeds 0.4, and 0.5 always falls in the unsure band. It is an easy target, and I say so here instead of crediting the system with more than it did.
5. All 15 appeals (5 on each of 3 trials) returned `under_review` and all 15 appear in `GET /log`. An appeal with an unknown `content_id` returned a 404 and the log held 197 entries both before and after. I tested this one by hand with curl because `scenarios.py` can only send text; it cannot submit and then appeal.

**Real output from trial 1**, from `run_eval.py::main` calling `app.py::submit`, with the combined score from `scoring.py::combine_signals` and the label from `scoring.py::score_to_label`.

Criterion 1, my own writing (two of the ten):

```json
[
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5836,
    "model_score": 0.706,
    "style_score": 0.502,
    "sent": "I feel very dejected and confused and I dont really like how my life i"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.3379,
    "model_score": 0.5231,
    "style_score": 0.2145,
    "sent": "The aim is to build a novel data science system to evaluate applicants"
  }
]
```

Criterion 2, a clearly-AI text and a clearly-human text:

```json
[
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.691,
    "model_score": 0.8855,
    "style_score": 0.5613,
    "sent": "The Big Bang Theory is the scientific explanation for how the universe"
  }
]
[
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5029,
    "model_score": 0.5445,
    "style_score": 0.4752,
    "sent": "We are plannign a trip to texas to attend our friend's wedding. It is "
  }
]
```

Criterion 3, label coverage (all three):

```json
[
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.691,
    "model_score": 0.8855,
    "style_score": 0.5613,
    "label": "This may have been written with an AI tool. We can get this wrong, especially with plain or simple writing. If you wrote it yourself, tell us and a person will review it.",
    "sent": "The Big Bang Theory is the scientific explanation for how the universe"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5,
    "model_score": 0.5364,
    "style_score": 0.0747,
    "label": "We can't tell for sure whether this was written by a person or with an AI tool. This isn't a finding that anything is wrong. If you'd like someone to take a look, you can send us a note.",
    "sent": "Honestly, I didn't expect remote work to change my routine this much. "
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.3379,
    "model_score": 0.5231,
    "style_score": 0.2145,
    "label": "This looks like it was written by a person.",
    "sent": "The aim is to build a novel data science system to evaluate applicants"
  }
]
```

Criterion 4, two texts from the gap rule scenario (the first has a gap of 0.53, the second 0.32):

```json
[
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5,
    "model_score": 0.7063,
    "style_score": 0.1809,
    "sent": "For any data science system, the crucial component is data. We need to"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.691,
    "model_score": 0.8855,
    "style_score": 0.5613,
    "sent": "The Big Bang Theory is the scientific explanation for how the universe"
  }
]
```

Criterion 5, the first three of the fifteen appeals from `results/appeal_check_before.txt` (produced by `app.py::appeal`), then the checks:

```
trial 1 appeal 1: { "content_id": "20de4cbb-ad58-4fac-be1c-df7efb2b1e40", "message": "Thanks. Your appeal has been recorded and a person will review it.", "status": "under_review"}
trial 1 appeal 2: { "content_id": "3fba42d4-f548-4eff-9b60-3bc37a50915f", "message": "Thanks. Your appeal has been recorded and a person will review it.", "status": "under_review"}
trial 1 appeal 3: { "content_id": "954a42a1-9fa8-4fb0-9743-39cf056a5f4c", "message": "Thanks. Your appeal has been recorded and a person will review it.", "status": "under_review"}
appeals found in GET /log for appeal_eval_* creators: 15
unknown content_id -> HTTP 404; log entries before: 197, after: 197
```

**Diagnoses**

1. **Criterion 2 missed. Stage: the combining rule, over signal two.** On these ten paragraphs, signal one alone separated AI from human by 0.409 (0.813 against 0.404) and signal two alone by only 0.136 (0.510 against 0.374). My rule weights signal two at 0.6, a choice I made in unit 7 from ten short texts, so the weaker signal dominated and cut the gap to 0.236. A secondary cause is signal one on the weather paragraph: its numbers and symbols (79°F, (26°C)) raise perplexity, so the model scored it only 0.424.

2. **All ten evasion attacks got through. Stages: signal two, mostly, and signal one.** Signal two scored 6 of the 10 below 0.35. The attacks (broken-up sentences, a pasted quotation, a human paragraph bolted on, one very long and one very short sentence, repeated stanzas) change sentence lengths, and sentence spread carries 70% of the style score, so the signal reads the change as human. Signal one fails differently: typos (EV01) and very short text (EV08) pulled its score down to 0.16 and 0.25.

3. **None of the 56 attacks was labeled AI. Stage: signal two, plus its 0.6 weight.** Signal two reads almost everything as human. Its average was 0.27 on the evasion inputs, 0.31 on the false-positive inputs and 0.12 on the injection inputs, against 0.51 on the unedited AI paragraphs. With 60% of the weight on a signal that low, the AI label only fires when an unmodified AI paragraph is both very predictable and shaped like AI. I also checked whether my disagreement rule was to blame, since it forced EV02, EV03, EV09 and EV10 to 0.5. It was not: without the rule they would have scored 0.32, 0.33, 0.34 and 0.58, none of them above the 0.65 AI line, and three would have been labeled human instead of unsure.

4. **FP08, my worst outcome. Stage: the route.** `MIN_WORDS = 10` in `app.py` refused an eight-word genuine submission with a 400. No decision means no `content_id`, so the writer had nothing to appeal.

5. **PI01 and PI02, labeled human. Stages: signal one and signal two, the same mechanism as the evasion attacks.** Nothing in my pipeline reads instructions, so no instruction was obeyed. The injected prefixes changed the text's statistics: the model score on the same underlying paragraph ranged from 0.20 (the "SYSTEM:" prefix) to 0.64 depending on the prefix, and signal two scored below 0.2 on all six injection inputs.

6. **RQ10 and RQ11: untested.** Both were rate limited as my own address before reaching the route, so I do not know what the route does with them.

**The pattern.** Diagnoses 1, 2, 3 and 5 are one problem: signal two is a weak signal carrying 60% of the combined score. FP08 is a separate one, in the route.

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
