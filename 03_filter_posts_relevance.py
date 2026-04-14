"""
03_filter_inclusion_terms.py

Purpose:
Filter post-level and comment-level datasets using a simple inclusion rule:

INCLUDE if:
    (contains at least one LLM/AI chatbot term)
    AND
    (contains at least one mental health term)

Why this matters:
- LLM terms alone pull lots of technical noise (prompting, coding, model debates).
- Mental health terms alone pull general mental health discussions unrelated to AI.
- Requiring BOTH isolates posts/comments discussing LLM-based chatbots in a mental health context.

Inputs:
- data_processed/*_posts.csv
- data_processed/*_comments.csv

Outputs:
- data_filtered/*_posts_filtered.csv
- data_filtered/*_comments_filtered.csv
"""

import os
import re
import pandas as pd

DATA_IN = "data_processed"
DATA_OUT = "data_filtered"
os.makedirs(DATA_OUT, exist_ok=True)

# -------------------------
# 1) Keyword dictionaries
# -------------------------
AI_TERMS = [
    r"\bchatgpt\b", r"\bgpt[- ]?3\.?5\b", r"\bgpt[- ]?4(o)?\b", r"\bgpt\b",
    r"\bclaude\b", r"\bgemini\b", r"\bbard\b", r"\bllm\b", r"\blarge language model\b",
    r"\bai chatbot\b", r"\bchatbot\b", r"\btherapy\s?gpt\b", r"\btherapist ai\b"
]

MH_TERMS = [
    r"\banxiety\b", r"\bpanic\b", r"\bdepress(ed|ion)?\b", r"\bstress(ed)?\b",
    r"\blonely|loneliness\b", r"\btrauma(tic)?\b", r"\bsuicid(al|e)\b",
    r"\bself[- ]?harm\b", r"\bmental health\b", r"\btherapy\b", r"\btherapist\b",
    r"\bemotional support\b", r"\bcoping\b", r"\bburnout\b", r"\bgrief\b"
]

# Optional: experiential signals (reduces “general discussion” noise)
EXPERIENCE_TERMS = [
    r"\bi\b", r"\bmy\b", r"\bme\b", r"\bpersonally\b",
    r"\bi used\b", r"\bi've used\b", r"\bi tried\b", r"\bhelped me\b",
    r"\bit helped\b", r"\bi feel\b", r"\bi felt\b", r"\btalked to\b",
    r"\busing (chatgpt|gpt|claude|gemini)\b"
]

AI_RE = re.compile("|".join(AI_TERMS), flags=re.IGNORECASE)
MH_RE = re.compile("|".join(MH_TERMS), flags=re.IGNORECASE)
EXP_RE = re.compile("|".join(EXPERIENCE_TERMS), flags=re.IGNORECASE)

# -------------------------
# 2) Helper functions
# -------------------------
def build_text(df: pd.DataFrame, cols: list[str]) -> pd.Series:
    """Safely concatenates relevant text columns."""
    existing = [c for c in cols if c in df.columns]
    if not existing:
        return pd.Series([""] * len(df))
    return (
        df[existing]
        .fillna("")
        .astype(str)
        .agg(" ".join, axis=1)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

def apply_filters(df: pd.DataFrame, text_col: str, *,
                  min_chars: int,
                  require_experience: bool,
                  max_chars: int | None = None) -> pd.DataFrame:
    """AND-based relevance filter + quality gates."""
    text = df[text_col].fillna("").astype(str)

    # AND condition: must match BOTH AI and MH
    mask = text.str.contains(AI_RE) & text.str.contains(MH_RE)

    # Minimum length
    mask &= text.str.len().ge(min_chars)

    # Optional experiential filter
    if require_experience:
        mask &= text.str.contains(EXP_RE)

    out = df.loc[mask].copy()

    # Optional max length cap (truncate instead of drop, keeps narratives but manageable)
    if max_chars is not None:
        out[text_col] = out[text_col].str.slice(0, max_chars)

    return out

# -------------------------
# 3) File map
# -------------------------
SUBREDDITS = ["chatgpt", "therapygpt", "mentalhealth", "anxiety"]

for sub in SUBREDDITS:
    print(f"\n--- Filtering {sub} ---")

    posts_path = os.path.join(DATA_IN, f"{sub}_posts.csv")
    comments_path = os.path.join(DATA_IN, f"{sub}_comments.csv")  

    # ---- POSTS ----
    posts = pd.read_csv(posts_path, low_memory=False)
    posts["text_for_filter"] = build_text(posts, ["title", "body"])

    # For r/ChatGPT: require experiential signals (recommended)
    require_exp_posts = True if sub == "chatgpt" else False

    posts_f = apply_filters(
        posts,
        "text_for_filter",
        min_chars=80,              # posts should have some substance
        require_experience=require_exp_posts,
        max_chars=6000             # cap extreme monologues but keep the content
    )

    posts_out = os.path.join(DATA_OUT, f"{sub}_posts_filtered.csv")
    posts_f.drop(columns=["text_for_filter"], errors="ignore").to_csv(posts_out, index=False)

    print(f"Posts: {len(posts):,} → {len(posts_f):,}  | saved: {posts_out}")

    # ---- COMMENTS ----
    comments = pd.read_csv(comments_path, low_memory=False)
    comments["text_for_filter"] = build_text(comments, ["comment_body"])

    # Comments: min_chars higher removes “try GPT-4o” spammy short replies
    comments_f = apply_filters(
        comments,
        "text_for_filter",
        min_chars=40,
        require_experience=False,  # usually too strict for comments
        max_chars=1200
    )

    comments_out = os.path.join(DATA_OUT, f"{sub}_comments_filtered.csv")
    comments_f.drop(columns=["text_for_filter"], errors="ignore").to_csv(comments_out, index=False)

    print(f"Comments: {len(comments):,} → {len(comments_f):,} | saved: {comments_out}")