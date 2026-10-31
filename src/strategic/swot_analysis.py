from __future__ import annotations


def generate_pest_analysis(project_name, political=0.5, economic=0.5, social=0.5, technological=0.5):
    factors = {
        "political": political,
        "economic": economic,
        "social": social,
        "technological": technological,
    }

    return {
        "project_name": project_name,
        "factors": factors,
        "summary": (
            f"{project_name} shows a balanced external environment. "
            f"Political conditions are {factors['political']:.2f}, economic conditions are {factors['economic']:.2f}, "
            f"social conditions are {factors['social']:.2f}, and technology conditions are {factors['technological']:.2f}."
        ),
        "overall_score": round(sum(factors.values()) / len(factors), 2),
    }
