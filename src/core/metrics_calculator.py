from __future__ import annotations


def build_cashflow(investment, annual_revenue, annual_cost, growth_rate, years, discount_rate=0.1):
    if investment <= 0:
        raise ValueError("Initial investment must be greater than zero.")

    cashflows = [-float(investment)]
    revenue = float(annual_revenue)
    cost = float(annual_cost)
    growth = float(growth_rate)
    discount = float(discount_rate)

    for year in range(1, int(years) + 1):
        projected_revenue = revenue * ((1 + growth) ** year)
        projected_cost = cost * ((1 + growth * 0.7) ** year)
        operating_cashflow = max(projected_revenue - projected_cost, 0.0)
        discounted_cashflow = operating_cashflow / ((1 + discount) ** year)
        cashflows.append(float(discounted_cashflow))

    return cashflows


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
