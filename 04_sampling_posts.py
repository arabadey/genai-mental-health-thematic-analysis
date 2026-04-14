""""
04_sampling_posts.py

Purpose: 
- To extract a sample from each of the subreddit datasets (specifically 75 from each in this case) to conduct inductive thematic analysis.
- Will be geared towards posts not comments, as the main focus for thematic analysis are the posts (comments will be covered by sentiment analysis).
- Once .csvs are sampled randomely to the correct amount (75 each) the csv file will be then converted to an excel file to view properly for thematic analysis.

Inputs: 
- data_filtered_/*_posts_filtered.csv

Outputs: 
- Thematic_sample_300.xlsx
"""
import os
import pandas as pd

FILTERED_DIR = "data_filtered"
out_path = "sample"
SAMPLE_SIZE = 75
RANDOM_SEED = 42

subreddits = ["chatgpt", "therapygpt", "mentalhealth", "anxiety"]

samples = []

for sub in subreddits:
    print(f"\n--- Sampling {sub} ---")

    path = os.path.join(FILTERED_DIR, f"{sub}_posts_filtered.csv")
    df = pd.read_csv(path, low_memory=False)

    if len(df) < SAMPLE_SIZE:
        sample_df = df.copy()
    else:
        sample_df = df.sample(n=SAMPLE_SIZE, random_state=RANDOM_SEED)

    sample_df["source_subreddit"] = sub
    samples.append(sample_df)

combined_sample = pd.concat(samples, ignore_index=True)

# CLEAN TEXT FOR DISPLAY (important)
combined_sample["title"] = combined_sample["title"].astype(str).str.replace("\n", " ", regex=False)
combined_sample["body"] = combined_sample["body"].astype(str).str.replace("\n", " ", regex=False)

# Save as Excel instead of CSV
out_path = os.path.join(out_path, "thematic_sample_300.xlsx")
combined_sample.to_excel(out_path, index=False)

print(f"\nSaved clean Excel file to: {out_path}")