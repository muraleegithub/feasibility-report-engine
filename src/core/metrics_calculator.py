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
