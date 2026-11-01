from src.engine import generate_project_report


def test_generate_project_report_basics():
    payload = {
        "project_name": "Test Feasibility",
        "investment": 100000,
        "annual_revenue": 50000,
        "annual_cost": 25000,
        "growth_rate": 0.08,
        "years": 5,
        "currency": "USD",
        "discount_rate": 0.1,
        "scenario": "base",
    }

    report = generate_project_report(payload)
    assert report["project_name"] == "Test Feasibility"
    assert "metrics" in report
    assert "cashflow" in report
    assert "risk" in report
    assert "strategic" in report
    assert report["metrics"]["npv"] is not None
    assert report["metrics"]["irr"] >= -100
