# Milestone 1 notes — tracing a submission

## A. The path of a submission

1. `app.py::submit` receives `{text, creator_id}`, rejects bad input, and makes a `content_id` (a uuid).
2. `detector.py::model_signal` returns `model_score`, 0-1.
3. `stylometry.py::style_signal` returns `style_score`, 0-1.
4. `scoring.py::combine_signals` returns one combined score, 0-1. This is the `confidence`.
5. `scoring.py::score_to_label` returns the `guess` (ai / human / unsure) and the label text.
6. `audit.py::log_decision` appends the decision (all three scores, label, status `decided`) to `logs/audit.jsonl`.
7. `/submit` returns JSON with `content_id`, `guess`, `confidence`, `label`, `model_score`, `style_score`.

## B. The two signals

| | Signal one (model) | Signal two (style) |
|---|---|---|
| Measures | How predictable the words are to a language model (perplexity) | Sentence-length spread, word variety, punctuation density |
| Why it might differ | AI picks likely next words, so its text is predictable. Human text is more surprising | AI tends toward even sentences and a narrow vocabulary. Humans are lumpier |
| Can't see | Authorship. Plain, common-word writing scores AI-like even when a person wrote it (second-language and younger writers). Dense, ornate prose scores human | Meaning. Typos and chopped sentences make AI text look human, and that is cheap to do on purpose |

## C. The false positive

A second-language writer submits their own poem.

1. Signal one scores it high (about 0.85) because the words are simple and predictable. Signal two also scores it high (about 0.75) because the sentences are short and even.
2. The combined score is about 0.8, above AI_THRESHOLD (0.65). They get the high-confidence AI label.
3. The label must tell them they can appeal: POST /appeal with their content_id and their reasoning. The item moves to under_review and the appeal is logged next to the original decision.

Consequence for thresholds: keep the unsure band wide and the AI threshold high (around 0.75), so only clearly machine-like text is accused.

## D. Endpoint contracts

### POST /submit
- In: `{"text": string, "creator_id": string}`
- Out (200): `{"content_id", "guess", "confidence", "label", "model_score", "style_score"}`
- Errors: 400 if text or creator_id is missing, not a string, or empty; 400 if text is under 10 words; 413 if text is over 10,000 characters. Error body: `{"error": "...", "message": "..."}`. Rejections are logged.

### POST /appeal
- In: `{"content_id": string, "reasoning": string}`
- Out (200): `{"content_id", "status": "under_review", "message": "..."}`
- Errors: 400 if either field is missing or empty; 404 if the content_id is not in the log.
