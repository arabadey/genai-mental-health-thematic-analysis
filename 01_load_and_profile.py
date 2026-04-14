"""
01_load_and_profile.py

Purpose:
Before performing any cleaning or filtering, I first profile each subreddit dataset
to understand its true structure and scale.

Because the collaborator provided flattened CSV files (where each row represents
a post-comment pair), a single post may appear multiple times—once for each comment.

Therefore, I compute:
- Total rows (post-comment pairs)
- Unique post IDs (true number of posts)
- Unique comment IDs (true number of comments)

This step allows me to determine:
1. The actual analytic corpus size.
2. Whether deduplication is necessary.
3. The proportion of comments relative to posts.
"""

import os
import pandas as pd

# Define the folder containing the raw CSV files
RAW_DIR = "data_raw"

# Define the folder containing the raw CSV files (From data_raw folder)
files = [
    "chatgpt_flat.csv",
    "therapygpt_flat.csv",
    "mentalhealth_flat.csv",
    "anxiety_flat.csv"
]

# Loop through each file and compute basic structural metrics
for file in files:
    print(f"/n--- Profiling {file} ---")

    # Construct full file path
    path = os.path.join(RAW_DIR, file)

    # Load CSV with low_memory=False to avoid mixed dtype warnings (Memory loaded all at once vs in smaller chunks)
    df = pd.read_csv(path, low_memory=False)

    # Total Rows represent the post-comment pairs
    print(f"Total Rows: {len(df):,}")

    # Unique post IDs represent the true number of posts
    print(f"Unique Posts: {df['post_id'].nunique():,}")

    # Unique comment IDs represent the true number of comments
    print(f"Unique Comments: {df['comment_id'].nunique():,}")

    # Prints column structure to confirm expected variables
    print("Columns detected:", df.columns.tolist())