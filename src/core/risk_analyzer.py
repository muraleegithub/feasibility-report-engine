from __future__ import annotations

import math


def calculate_metrics(cashflows):
    if not cashflows:
        return {"npv": 0.0, "irr": 0.0, "roi": 0.0, "payback_period": 0.0}

    total_investment = abs(float(cashflows[0]))
    inflows = [value for value in cashflows[1:] if value > 0]
    roi_value = ((sum(inflows) - total_investment) / total_investment * 100) if total_investment else 0.0

    npv_value = 0.0
    for idx, value in enumerate(cashflows):
        npv_value += value / ((1.10) ** idx)

    def irr_function(rate):
        return sum(cf / ((1 + rate) ** idx) for idx, cf in enumerate(cashflows))

    low = -0.9999
    high = 10.0
    for _ in range(200):
        mid = (low + high) / 2.0
        if irr_function(mid) > 0:
            low = mid
        else:
            high = mid

    payback = 0.0
    cumulative = 0.0
    for idx, value in enumerate(cashflows[1:], start=1):
        cumulative += value
        if cumulative >= 0:
            payback = float(idx)
            break

    return {
        "npv": round(npv_value, 2),
        "irr": round(((low + high) / 2.0) * 100, 2),
        "roi": round(roi_value, 2),
        "payback_period": round(payback, 2),
        "total_cashflow": round(sum(cashflows), 2),
        "discounted_cashflow": round(npv_value, 2),
    }
