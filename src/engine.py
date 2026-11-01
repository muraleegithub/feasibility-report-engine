from __future__ import annotations

from src.core.financial_model import build_cashflow
from src.core.metrics_calculator import calculate_metrics
from src.core.risk_analyzer import evaluate_risk
from src.inputs.data_validator import validate_project_input
from src.strategic.pest_analysis import generate_pest_analysis
from src.strategic.swot_analysis import generate_swot_analysis


def generate_project_report(raw_data):
    project = validate_project_input(raw_data)

    cashflows = build_cashflow(
        investment=project["investment"],
        annual_revenue=project["annual_revenue"],
        annual_cost=project["annual_cost"],
        growth_rate=project["growth_rate"],
        years=project["years"],
        discount_rate=project["discount_rate"],
    )
    metrics = calculate_metrics(cashflows)
    risk = evaluate_risk(cashflows, project.get("risk_adjustment", 0.1))
    pest = generate_pest_analysis(
        project_name=project["project_name"],
        political=project.get("political", 0.5),
        economic=project.get("economic", 0.5),
        social=project.get("social", 0.5),
        technological=project.get("technological", 0.5),
    )
    swot = generate_swot_analysis(
        project.get("strengths", []),
        project.get("weaknesses", []),
        project.get("opportunities", []),
        project.get("threats", []),
    )

    summary = (
        f"{project['project_name']} shows an estimated {metrics['roi']:.1f}% ROI with "
        f"NPV of {metrics['npv']:.2f} {project['currency']} over {project['years']} years. "
        f"The project is classified as {risk['category']} risk."
    )

    return {
        "project_name": project["project_name"],
        "currency": project["currency"],
        "scenario": project["scenario"],
        "summary": summary,
        "cashflow": cashflows,
        "metrics": metrics,
        "risk": risk,
        "strategic": {
            "pest": pest,
            "swot": swot,
        },
    }
