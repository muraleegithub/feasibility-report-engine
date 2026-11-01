def generate_pest_analysis(project_name, political=0.5, economic=0.5, social=0.5, technological=0.5):
    return {
        "project_name": project_name,
        "summary": (
            f"PEST review for {project_name}: political={political}, economic={economic}, "
            f"social={social}, technological={technological}."
        ),
        "political": political,
        "economic": economic,
        "social": social,
        "technological": technological,
    }
