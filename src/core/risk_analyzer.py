from __future__ import annotations

from src.core.metrics_calculator import calculate_metrics


def evaluate_risk(cashflows, risk_adjustment=0.1):
    metrics = calculate_metrics(cashflows)
    if metrics["irr"] >= 15:
        category = "Low"
    elif metrics["irr"] >= 5:
        category = "Medium"
    else:
        category = "High"

    score = min(100, max(0, int((100 - metrics["irr"]) * risk_adjustment)))
    return {
        "category": category,
        "score": score,
        "summary": f"Risk score is {score} based on projected IRR and risk adjustment.",
        "metrics": metrics,
    }
