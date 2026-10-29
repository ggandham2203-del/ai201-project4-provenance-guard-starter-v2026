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

**My limits:** ___ per minute, ___ per day

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
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

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
