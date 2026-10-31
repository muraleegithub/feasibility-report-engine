from __future__ import annotations


def generate_swot_analysis(strengths, weaknesses, opportunities, threats):
    return {
        "strengths": strengths or [],
        "weaknesses": weaknesses or [],
        "opportunities": opportunities or [],
        "threats": threats or [],
        "summary": "The initiative balances internal strengths and external opportunities against key weaknesses and threats.",
    }
