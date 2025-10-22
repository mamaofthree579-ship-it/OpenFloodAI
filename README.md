# 🌊 OpenFloodAI
**OpenFloodAI** is an open-source initiative to improve flood-risk forecasting using transparent, community-driven tools.  
The project blends meteorological, hydrological, and climate-signal inputs into probabilistic forecasts that update automatically each day.

---

## 🚀 Features
- **Automated Forecasts:** Runs daily through GitHub Actions.
- **Hybrid Algorithm:** Combines ensemble probabilities, seasonal signals (ENSO, PDO), and coastal multipliers.
- **Open Data Pipeline:** Outputs machine-readable results to `/data/outputs/latest_forecast.json`.
- **Live Dashboard:**  
  [🌐 View Current Forecast](https://mamaofthree579-ship-it.github.io/OpenFloodAI/)

---

## 🧠 How It Works
1. The workflow installs dependencies from `requirements.txt`.
2. `flood_predictor_runner.py` executes the forecast model.
3. Results are saved to `data/outputs/latest_forecast.json`.
4. The public dashboard reads and displays the latest results.

Example logic excerpt:
```python
if ENSO_bias >= +0.4 and PDO_pos and AR_cat >= 3 and hydrologic_load >= HIGH:
    escalate_seasonal_tilt += 0.15
P_final = clamp(ensemble_prob * (1 + seasonal_tilt) * coastal_multiplier, 0, 1)
