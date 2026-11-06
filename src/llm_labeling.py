"""Prepare batches for LLM labeling and merge the results back.

The 1,000-review sample is split into batches of review texts with short ids
(r0001...). Each batch is labeled by a fresh LLM session that only sees the
prompt (docs/review_analysis/03_labeling_prompt.md), the taxonomy and the batch.
The labeled JSONL files are then validated and merged into one CSV.

Usage:
    python src/llm_labeling.py prepare <batch_dir>
    python src/llm_labeling.py merge <batch_dir>
"""
import json
import sys
from pathlib import Path

import pandas as pd

SAMPLE = Path("outputs/negative_reviews_sample_1000.csv")
OUTPUT = Path("data/labels/llm_labels_1000.csv")
BATCH_SIZE = 250
LABELS = {
    "not_received", "late_delivery", "incomplete_order", "wrong_product", "damaged_or_defective",
    "poor_quality_or_not_as_described", "cancellation_or_refund", "delivery_service",
    "customer_service", "other_or_unclear",
}


def load_sample():
    sample = pd.read_csv(SAMPLE)
    sample["id"] = [f"r{i:04d}" for i in range(1, len(sample) + 1)]
    return sample


def prepare(batch_dir):
    batch_dir.mkdir(parents=True, exist_ok=True)
    sample = load_sample()
    for n, start in enumerate(range(0, len(sample), BATCH_SIZE), 1):
        batch = sample.iloc[start:start + BATCH_SIZE]
        with open(batch_dir / f"batch_{n}_input.jsonl", "w", encoding="utf-8") as f:
            for row in batch.itertuples():
                f.write(json.dumps({"id": row.id, "text": row.review_text}, ensure_ascii=False) + "\n")
    print(f"Wrote {n} batches of up to {BATCH_SIZE} reviews to {batch_dir}")


def merge(batch_dir):
    sample = load_sample()
    rows = []
    for path in sorted(batch_dir.glob("batch_*_labels.jsonl")):
        with open(path, encoding="utf-8") as f:
            rows += [json.loads(line) for line in f if line.strip()]
    labels = pd.DataFrame(rows).drop_duplicates("id")

    missing = set(sample["id"]) - set(labels["id"])
    invalid = labels[~labels["primary_label"].isin(LABELS)]
    if missing or len(invalid):
        raise SystemExit(f"{len(missing)} reviews missing, {len(invalid)} invalid labels: fix before merging")

    merged = sample[["id", "review_id", "review_text"]].merge(labels, on="id")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    merged.drop(columns="id").to_csv(OUTPUT, index=False)
    print(f"Merged {len(merged):,} labels into {OUTPUT}")
    print(merged["primary_label"].value_counts().to_string())


if __name__ == "__main__":
    command, batch_dir = sys.argv[1], Path(sys.argv[2])
    {"prepare": prepare, "merge": merge}[command](batch_dir)
