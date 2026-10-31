from __future__ import annotations


def validate_project_input(payload):
    if not isinstance(payload, dict):
        raise ValueError("Project payload must be a JSON object.")

    project_name = payload.get("project_name") or "Untitled Feasibility Study"
    investment = float(payload.get("investment", 0.0) or 0.0)
    annual_revenue = float(payload.get("annual_revenue", 0.0) or 0.0)
    annual_cost = float(payload.get("annual_cost", 0.0) or 0.0)
    growth_rate = float(payload.get("growth_rate", 0.05) or 0.05)
    years = int(payload.get("years", 5) or 5)
    currency = payload.get("currency", "USD")
    scenario = payload.get("scenario", "base")
    discount_rate = float(payload.get("discount_rate", 0.10) or 0.10)

    return {
        "project_name": project_name,
        "investment": investment,
        "annual_revenue": annual_revenue,
        "annual_cost": annual_cost,
        "growth_rate": growth_rate,
        "years": max(1, years),
        "currency": currency,
        "scenario": scenario,
        "discount_rate": discount_rate,
        "political": float(payload.get("political", 0.5) or 0.5),
        "economic": float(payload.get("economic", 0.5) or 0.5),
        "social": float(payload.get("social", 0.5) or 0.5),
        "technological": float(payload.get("technological", 0.5) or 0.5),
        "risk_adjustment": float(payload.get("risk_adjustment", 0.1) or 0.1),
        "strengths": payload.get("strengths", []) or [],
        "weaknesses": payload.get("weaknesses", []) or [],
        "opportunities": payload.get("opportunities", []) or [],
        "threats": payload.get("threats", []) or [],
    }
