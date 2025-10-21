"""
OpenFloodAI Dashboard Builder
Generates a simple HTML page from the forecast JSON.
"""

import json
from datetime import datetime
from pathlib import Path

def build_dashboard():
    data_path = Path("data/outputs/all_forecasts.json")
    if not data_path.exists():
        print("⚠️ No forecast file found. Run scripts/flood_predictor_runner.py first.")
        return

    with open(data_path, "r") as f:
        forecasts = json.load(f)

    timestamp = forecasts.get("timestamp", "Unknown time")
    regions = forecasts.get("forecasts", {})

    html_lines = [
        "<html><head><title>OpenFloodAI Dashboard</title>",
        "<style>body{font-family:sans-serif;background:#eef;} .region{margin:10px;padding:10px;border:1px solid #ccc;border-radius:5px;} .RED{background:#f88;} .AMBER{background:#ffb347;} .GREEN{background:#aaffaa;}</style>",
        "</head><body>",
        f"<h1>🌊 OpenFloodAI Dashboard</h1>",
        f"<p>Last update: {timestamp}</p>"
    ]

    for name, info in regions.items():
        tier = info.get("tier", "GREEN")
        prob = info.get("P_final", 0)
        html_lines.append(f"<div class='region {tier}'><h2>{name}</h2>")
        html_lines.append(f"<p>Flood probability: {prob:.2f}</p>")
        html_lines.append(f"<p>Alert tier: <strong>{tier}</strong></p></div>")

    html_lines.append("</body></html>")

    output_path = Path("dashboard/index.html")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(html_lines), encoding="utf-8")

    print(f"✅ Dashboard built successfully at {output_path.resolve()}")

if __name__ == "__main__":
    build_dashboard()
