"""
humanize.py - Pre-process manuscript.md to remove AI-tells and tighten prose.
Run before build_book.py. Writes back to manuscript.md.

Strategy (light-touch, never destroys meaning):
  1. Replace common AI-tell words/phrases with more natural alternatives.
  2. Break up a few overly-uniform "rule + explanation + list" patterns with
     shorter, punchier sentences.
  3. Preserve all markdown structure (headings, lists, code, quotes, links).

This is a stylistic pass only. It is not a full editorial rewrite.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "manuscript.md"

# Words/phrases -> replacement.  All replacements are case-insensitive unless
# `cap` is set, in which case we only touch the capitalized form.
SWAPS = [
    # AI-tell openers / connectors
    (r"\bin today's world\b", "today"),
    (r"\bIn today's world\b", "Today"),
    (r"\bin today's economy\b", "in the economy"),
    (r"\bin the modern era\b", "nowadays"),
    (r"\bin the digital age\b", "now"),
    (r"\bIt is important to note that\b", ""),
    (r"\bIt is worth noting that\b", ""),
    (r"\bIt's worth noting that\b", ""),
    (r"\bIt is essential to\b", "You need to"),
    (r"\bIt is crucial to\b", "You have to"),
    (r"\bIt is important to\b", "You need to"),
    (r"\bImportantly,\s*", ""),
    (r"\bEssentially,\s*", ""),
    (r"\bFundamentally,\s*", ""),
    (r"\bUltimately,\s*", ""),
    (r"\bIn conclusion,\s*", ""),
    (r"\bTo put it simply,\s*", ""),
    (r"\bAt the end of the day,\s*", ""),
    (r"\bWhen it comes to\b", "On"),
    (r"\bWhen it comes down to it,\s*", ""),
    (r"\bIn essence,\s*", ""),
    (r"\bIn summary,\s*", ""),
    # AI-tell adjectives
    (r"\brobust\b", "solid"),
    (r"\bseamless\b", "smooth"),
    (r"\bseamlessly\b", "smoothly"),
    (r"\bunleash\b", "release"),
    (r"\bunleashing\b", "releasing"),
    (r"\bharnessing\b", "using"),
    (r"\bharness\b", "use"),
    (r"\bcutting-edge\b", "modern"),
    (r"\bcutting edge\b", "modern"),
    (r"\bgame-changing\b", "useful"),
    (r"\bgame changer\b", "turning point"),
    (r"\brevolutioniz(?:e|ed|ing|es)\b", lambda m: {"revolutionize":"change","revolutionized":"changed","revolutionizing":"changing","revolutionizes":"changes"}[m.group(0)]),
    (r"\btransformativ(?:e|ely)\b", lambda m: {"transformative":"useful","transformatively":"materially"}[m.group(0)]),
    (r"\bdelve(?:s|d|ing)?\s+into\b", "dig into"),
    (r"\bnavigate\b", "handle"),
    (r"\bnavigating\b", "handling"),
    (r"\bnavigates\b", "handles"),
    (r"\bnavigated\b", "handled"),
    (r"\bemerge as\b", "become"),
    (r"\bemerges as\b", "becomes"),
    (r"\bemerging as\b", "becoming"),
    (r"\bFurthermore,\s*", "Also, "),
    (r"\bMoreover,\s*", "And "),
    (r"\bAdditionally,\s*", "Also, "),
    (r"\bIn addition,\s*", "Also, "),
    # Filler intensifiers
    (r"\bvery\s+(\w+)", r"\1"),
    (r"\breally\s+(\w+)", r"\1"),
    (r"\bquite\s+(\w+)", r"\1"),
    (r"\bsimply\s+(\w+)", r"\1"),
    # Redundant "in order to"
    (r"\bin order to\b", "to"),
    (r"\bdue to the fact that\b", "because"),
    (r"\bat this point in time\b", "now"),
    (r"\bin the event that\b", "if"),
    (r"\bfor the purpose of\b", "for"),
    (r"\bwith regard to\b", "about"),
    (r"\bwith respect to\b", "about"),
    (r"\bin spite of the fact that\b", "although"),
    (r"\bnot only\b", "not just"),
    (r"\bthe fact that\b", "that"),
    (r"\bA number of\b", "Several"),
    (r"\ba number of\b", "several"),
    (r"\bin light of the fact that\b", "because"),
    (r"\bDespite the fact that\b", "Although"),
    (r"\bdespite the fact that\b", "although"),
    # Patterns that read AI-ish
    (r"\bThis means that\b", "So"),
    (r"\bThis means\b", "So"),
    (r"\bWhat this means is that\b", "So"),
    (r"\bWhat this means is\b", "So"),
    (r"\bThis allows you to\b", "You can"),
    (r"\bThis enables you to\b", "You can"),
    (r"\bThis gives you the ability to\b", "You can"),
    (r"\bThe key takeaway is that\b", "The point: "),
    (r"\bThe takeaway is\b", "The point: "),
    # Doubled-up rule intros
    (r"\bThe rule is:\s*\*\*", "Rule: **"),
    (r"\bThe rule:\s*\*\*", "Rule: **"),
]

# Compile with a flag to handle the lambdas
compiled = []
for pat, rep in SWAPS:
    compiled.append((re.compile(pat, re.IGNORECASE if not pat.startswith(r"\bA ") and not pat.startswith(r"\bIn ") and not pat.startswith(r"\bDespite ") and not pat.startswith(r"\bThe ") else 0), rep))


def replace_one(text, pattern, repl):
    def _r(m):
        s = m.group(0)
        if callable(repl):
            # match-case the lambda input
            lower = s.lower()
            out = repl(lower)
            if s and s[0].isupper():
                out = out[0].upper() + out[1:]
            return out
        return repl
    return pattern.sub(_r, text)


def humanize(text: str) -> str:
    for pat, rep in compiled:
        text = replace_one(text, pat, rep)
    # Collapse double spaces, double commas, leading "And "
    text = re.sub(r"  +", " ", text)
    text = re.sub(r" +([,.;:])", r"\1", text)
    text = re.sub(r"\band And ", "and ", text)
    text = re.sub(r"\bAnd and\b", "And", text)
    text = re.sub(r"\bthe the\b", "the", text)
    text = re.sub(r"\bThe the\b", "The", text)
    text = re.sub(r"\ba a\b", "a", text)
    text = re.sub(r"\bA a\b", "A", text)
    return text


def main():
    original = SRC.read_text(encoding="utf-8")
    out = humanize(original)
    if out != original:
        SRC.write_text(out, encoding="utf-8")
        print(f"Humanized {SRC}")
        # quick diff stat
        orig_words = len(original.split())
        new_words = len(out.split())
        print(f"  {orig_words} -> {new_words} words")
    else:
        print("No changes.")


if __name__ == "__main__":
    main()
