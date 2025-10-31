#!/usr/bin/env python3
"""
utils_validation.py - simple forecast validation tools
Computes Brier score and appends daily metrics to a CSV for tracking.
"""
import csv
from pathlib import Path
from typing import List

def brier_score(predictions: List[float], observations: List[float]) -> float:
    if len(predictions) != len(observations) or len(predictions) == 0:
        raise ValueError("Predictions and observations must be same non-zero length")
    return sum((p - o)**2 for p,o in zip(predictions, observations)) / len(predictions)

def append_validation_row(csv_path: str, date_str: str, region: str, brier: float):
    Path(csv_path).parent.mkdir(parents=True, exist_ok=True)
    exists = Path(csv_path).exists()
    with open(csv_path, "a", newline='') as f:
        writer = csv.writer(f)
        if not exists:
            writer.writerow(["date","region","brier_score"])
        writer.writerow([date_str, region, f"{brier:.6f}"])

if __name__ == "__main__":
    # small self-test
    preds = [0.2,0.5,0.7]
    obs = [0,1,1]
    print("Brier:", brier_score(preds, obs))
