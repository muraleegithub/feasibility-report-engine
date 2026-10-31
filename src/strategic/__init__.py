from __future__ import annotations


def evaluate_risk(cashflows, risk_adjustment=0.1):
    if not cashflows:
        return {"score": 0, "category": "low", "summary": "No cashflow data available."}

    absolute_values = [abs(value) for value in cashflows]
    average = sum(absolute_values) / len(absolute_values)
    volatility = sum(abs(value - average) for value in absolute_values) / len(absolute_values)
    score = min(100, max(0, round((volatility / max(average, 1.0)) * 100 + (risk_adjustment * 100), 2)))

    if score < 35:
        category = "low"
    elif score < 70:
        category = "medium"
    else:
        category = "high"

    return {
        "score": score,
        "category": category,
        "summary": (
            f"The modeled risk is {category} based on a score of {score} out of 100. "
            "Sensitivity to revenue volatility and external uncertainty should be monitored."
        ),
    }
