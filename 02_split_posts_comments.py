"""
02_split_posts_comments.py

Purpose:
The provided datasets are flattened such that each row contains:
- Post-level information (post_id, title, body, post metadata)
- Comment-level information (comment_id, comment_body, comment metadata)

Because thematic analysis will focus primarily on post narratives,
I separate the data into two distinct datasets:

1. A post-level dataset (One row per post_id)
2. A comment-level dataset (One row per comment_id)

This ensures:
- No post is overrepresented due to multiple comments.
- Clean units of analysis for thematic coding.
- Comments can optionally be used later for sentiment analysis.
"""

import os
import pandas as pd

RAW_DIR = "data_raw"
PROCESSED_DIR = "data_processed"

# Ensure processed folder exists
os.makedirs(PROCESSED_DIR, exist_ok=True)

files = [
    "chatgpt_flat.csv",
    "therapygpt_flat.csv",
    "mentalhealth_flat.csv",
    "anxiety_flat.csv"
]
# Define the columns for each output.
POST_COLS = [
    "post_id",
    "subreddit",
    "title",
    "body",
    "post_created_utc",   # or "created_utc" if that's what your file uses
    "score",
    "num_comments_field", # or "num_comments" depending on your file
]

COMMENT_COLS = [
    "comment_id",
    "post_id",
    "subreddit", 
    "comment_body",
    "comment_created_utc",  # or "created_utc" if comment uses the same name
    "comment_score",        # if present
]

# Same use of for loop to go through each csv to produce seperate datasets for post_id and comment_id
for file in files:
    print(f"/n--- Processing {file} ---")

    path = os.path.join(RAW_DIR, file)

    # Load raw flattened dataset
    df = pd.read_csv(path, low_memory=False, dtype=str)

    # -----------------------------
    # Step 1: Create Post-Level Dataset
    # -----------------------------
    # Because each post may appear once per comment
    # I drop the duplicates based on post_id to retain one row per post.
    # Also I will remove deleted or blank post bodies

    posts = df.drop_duplicates(subset="post_id", keep="first").copy()

    # Keep ONLY the post columns that exist in this file
    post_cols_present = [c for c in POST_COLS if c in posts.columns]
    posts = posts[post_cols_present].copy()

    # Remove deleted or blank post bodies
    for col in ["title", "body"]:
        if col in posts.columns:
            posts[col] = posts[col].fillna("").astype(str)

    if "title" in posts.columns and "body" in posts.columns:
        posts = posts[~((posts["title"].str.strip() == "") & (posts["body"].str.strip() == ""))]

    # Save Post-level dataset to path (PROCESSED_DIR)
    post_output = os.path.join(
        PROCESSED_DIR,
        file.replace("flat.csv", "posts.csv")
    )

    posts.to_csv(post_output, index=False)
    print(f"Post-level rows after deduplication: {len(posts):,}")
    print(f"Saved post-level file: {post_output}")

    # -----------------------------
    # Step 2: Create Comment-Level Dataset
    # -----------------------------
    # Like posts, comments are uniquely identified by comment_id.
    # I repeat the same process froms to drop duplicates in comments to ensure there is only one row per comment
    # and remove deleted or blank comment bodies
    
    comments = df[df["comment_id"].notna()].copy()  # keeps only real comment rows
    comments = df.drop_duplicates(subset="comment_id", keep="first").copy()

    # Keep ONLY the comment columns that exist in this file
    comment_cols_present = [c for c in COMMENT_COLS if c in comments.columns]
    comments = comments[comment_cols_present].copy()

    # Remove deleted or blank comments
    if "comment_body" in comments.columns:
        comments["comment_body"] = comments["comment_body"].fillna("").astype(str)
        comments = comments[comments["comment_body"].str.strip() != ""]

    # Save Comment-level data to path
    comment_output = os.path.join(
        PROCESSED_DIR,
        file.replace("flat.csv", "comments.csv")
    )

    comments.to_csv(comment_output, index=False)
    print(f"Comment-level rows after deduplication: {len(comments):,}")
    print(f"Saved comment-level file: {comment_output}")