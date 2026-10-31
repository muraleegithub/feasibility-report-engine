from __future__ import annotations

from math import isclose


def _safe_percent(value):
    return 0.0 if value is None else float(value)


def build_cashflow(investment, annual_revenue, annual_cost, growth_rate, years, discount_rate=0.1):
    if investment <= 0:
        raise ValueError("Initial investment must be greater than zero.")

    cashflows = [-float(investment)]
    revenue = float(annual_revenue)
    cost = float(annual_cost)
    growth = float(growth_rate)

    for year in range(1, int(years) + 1):
        revenue = revenue * (1 + growth)
        cost = cost * (1 + (growth * 0.75))
        operating_cashflow = max(revenue - cost, 0.0)

        if year == 1:
            adjusted_cashflow = operating_cashflow * (1 - discount_rate * 0.1)
        else:
            adjusted_cashflow = operating_cashflow * (1 - (discount_rate * 0.05 * year))

        cashflows.append(float(adjusted_cashflow))

    return cashflows
