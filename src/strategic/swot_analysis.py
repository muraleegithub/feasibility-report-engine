def generate_swot_analysis(strengths=None, weaknesses=None, opportunities=None, threats=None):
    strengths = strengths or []
    weaknesses = weaknesses or []
    opportunities = opportunities or []
    threats = threats or []

    return {
        "summary": "SWOT analysis prepared using supplied strengths, weaknesses, opportunities, and threats.",
        "strengths": strengths,
        "weaknesses": weaknesses,
        "opportunities": opportunities,
        "threats": threats,
    }
