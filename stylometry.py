"""
Signal two: the style signal. ← YOU BUILD THIS IN MILESTONE 4

Signal one reads the text for meaning. This one measures it *as text* — the
shape of it, without understanding a word.

Three measures are stubbed below because the brief names those three. They are
stubs, not implementations: what they compute is yours, and so is how you
combine them.

    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how much punctuation, and how varied?

Why these might differ between human and AI writing: generated prose tends
toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is
lumpier — a three-word sentence next to a forty-word one.

⚠️ **The blind spot, which you have to name in Milestone 1.**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose, and unit 8's attack set will do it to you.

Build each function on its own and call it from a terminal before you wire
anything together:

    python stylometry.py "some text to look at"
"""

import re
import statistics


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())


# ── The three measures ───────────────────────────────────────────────────────
# Direction: for all three measures, HIGHER means more human.
# style_signal() flips them so its own output is higher = more likely AI.

MAX_WORDS_FOR_TTR = 100

# How each measure maps to a 0-1 "AI-ness" score. First guesses, to be tuned
# against real test texts in Milestone 4.
SPREAD_HUMAN_AT = 0.4     # spread at or above this scores as fully human
TTR_LOW, TTR_HIGH = 0.5, 0.9
PUNCT_HUMAN_AT = 0.15     # punctuation per word at or above this scores as human
W_SPREAD, W_TTR, W_PUNCT = 0.7, 0.15, 0.15   # spread did the real work on my test texts


def _clamp(x: float) -> float:
    return max(0.0, min(1.0, x))


def sentence_length_spread(text: str) -> float:
    """Stdev / mean of sentence lengths in words. Higher = more human.
    A text with fewer than two sentences has no spread, so it returns 0.0."""
    lengths = [len(words(s)) for s in sentences(text)]
    lengths = [n for n in lengths if n > 0]
    if len(lengths) < 2:
        return 0.0
    return statistics.stdev(lengths) / statistics.mean(lengths)


def type_token_ratio(text: str) -> float:
    """Unique words / total words over the first 100 words. Higher = more human."""
    ws = words(text)[:MAX_WORDS_FOR_TTR]
    if not ws:
        return 0.0
    return len(set(ws)) / len(ws)


def punctuation_density(text: str) -> float:
    """Commas, semicolons, colons, dashes, parentheses and quotes per word.
    Higher = more human."""
    ws = words(text)
    if not ws:
        return 0.0
    marks = re.findall(r'[,;:()"\u2014\u2013-]', text)
    return len(marks) / len(ws)


# ── Combining them ───────────────────────────────────────────────────────────

def style_signal(text: str) -> float:
    """0-1, higher = more likely AI. Each measure is flipped so low
    spread / low variety / low punctuation = AI-like, then weighted."""
    if not words(text):
        return 0.5
    if len([x for x in sentences(text) if words(x)]) < 2:
        ai_spread = 0.5  # one sentence has no spread: neutral, not an accusation
    else:
        ai_spread = 1 - _clamp(sentence_length_spread(text) / SPREAD_HUMAN_AT)
    ai_ttr = 1 - _clamp((type_token_ratio(text) - TTR_LOW) / (TTR_HIGH - TTR_LOW))
    ai_punct = 1 - _clamp(punctuation_density(text) / PUNCT_HUMAN_AT)
    score = W_SPREAD * ai_spread + W_TTR * ai_ttr + W_PUNCT * ai_punct
    return round(_clamp(score), 4)


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"punctuation_density      {punctuation_density(text)}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")
    print("\nAll zeros? These are stubs — Milestone 4 is where you build them.")
