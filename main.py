from src.engine import generate_project_report

if __name__ == "__main__":
    sample = {
        "project_name": "Sample Feasibility Study",
        "description": "Demo project for validation",
        "investment": 500000,
        "annual_revenue": 220000,
        "annual_cost": 120000,
        "growth_rate": 0.06,
        "years": 8,
        "discount_rate": 0.1,
        "currency": "USD",
        "scenario": "base",
        "political": 0.4,
        "economic": 0.6,
        "social": 0.5,
        "technological": 0.7,
        "strengths": ["Clear demand", "Experienced team"],
        "weaknesses": ["High upfront cost", "Limited brand awareness"],
        "opportunities": ["New market", "Partnerships"],
        "threats": ["Competition", "Regulatory changes"],
    }
    print(generate_project_report(sample))
