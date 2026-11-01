import csv
import json
import re
from io import BytesIO, StringIO

from flask import Flask, Response, jsonify, redirect, render_template, request, send_file, url_for
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from config.database import get_database_uri
from database.models import Project, Report, db, init_db
from src.engine import generate_project_report


def slugify(value: str) -> str:
    value = (value or "report").strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "report"


def report_payload(project: Project, report: Report | None) -> dict:
    metrics = (report.metrics if report and report.metrics else {}) if report else {}
    risk = (report.risk if report and report.risk else {}) if report else {}
    strategic = (report.strategic if report and report.strategic else {}) if report else {}
    summary = report.summary if report and report.summary else "No summary available yet."

    return {
        "project": {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "currency": project.currency,
            "investment": project.investment,
            "annual_revenue": project.annual_revenue,
            "annual_cost": project.annual_cost,
            "growth_rate": project.growth_rate,
            "years": project.years,
        },
        "summary": summary,
        "metrics": metrics,
        "risk": risk,
        "strategic": strategic,
    }


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = get_database_uri()
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JSON_SORT_KEYS"] = False

    init_db(app)

    @app.route("/")
    def index():
        projects = Project.query.order_by(Project.id.desc()).all()
        return render_template("index.html", projects=projects)

    @app.route("/projects/new", methods=["GET", "POST"])
    def new_project():
        if request.method == "POST":
            payload = {
                "project_name": request.form.get("project_name") or "Untitled Feasibility Study",
                "investment": float(request.form.get("investment", 0) or 0),
                "annual_revenue": float(request.form.get("annual_revenue", 0) or 0),
                "annual_cost": float(request.form.get("annual_cost", 0) or 0),
                "growth_rate": float(request.form.get("growth_rate", 0.05) or 0.05),
                "years": int(request.form.get("years", 5) or 5),
                "currency": request.form.get("currency", "USD"),
                "discount_rate": float(request.form.get("discount_rate", 0.10) or 0.10),
                "scenario": request.form.get("scenario", "base"),
                "political": float(request.form.get("political", 0.5) or 0.5),
                "economic": float(request.form.get("economic", 0.5) or 0.5),
                "social": float(request.form.get("social", 0.5) or 0.5),
                "technological": float(request.form.get("technological", 0.5) or 0.5),
                "strengths": request.form.getlist("strengths"),
                "weaknesses": request.form.getlist("weaknesses"),
                "opportunities": request.form.getlist("opportunities"),
                "threats": request.form.getlist("threats"),
            }

            report_data = generate_project_report(payload)

            project = Project(
                name=payload["project_name"],
                description=request.form.get("description", ""),
                currency=payload["currency"],
                investment=payload["investment"],
                annual_revenue=payload["annual_revenue"],
                annual_cost=payload["annual_cost"],
                growth_rate=payload["growth_rate"],
                years=payload["years"],
            )

            db.session.add(project)
            db.session.commit()

            report_entry = Report(
                project_id=project.id,
                summary=report_data["summary"],
                metrics=report_data["metrics"],
                risk=report_data["risk"],
                strategic=report_data["strategic"],
            )

            db.session.add(report_entry)
            db.session.commit()

            return redirect(url_for("report_detail", project_id=project.id))

        return render_template("project_form.html")

    @app.route("/projects/<int:project_id>")
    def report_detail(project_id):
        project = Project.query.get_or_404(project_id)
        report = Report.query.filter_by(project_id=project_id).order_by(Report.id.desc()).first()
        return render_template("report.html", project=project, report=report)

    @app.route("/projects/<int:project_id>/export")
    def export_report(project_id):
        project = Project.query.get_or_404(project_id)
        report = Report.query.filter_by(project_id=project_id).order_by(Report.id.desc()).first()
        data = report_payload(project, report)
        export_format = (request.args.get("format", "json") or "json").lower()
        filename = f"{slugify(project.name)}-report"

        if export_format == "json":
            return Response(
                json.dumps(data, indent=2),
                mimetype="application/json",
                headers={"Content-Disposition": f'attachment; filename="{filename}.json"'},
            )

        if export_format == "csv":
            csv_buffer = StringIO()
            writer = csv.writer(csv_buffer)
            metrics = data.get("metrics") or {}
            risk = data.get("risk") or {}
            writer.writerow(["project", "summary", "npv", "irr", "roi", "payback_period", "risk_category", "risk_score"])
            writer.writerow([
                project.name,
                data.get("summary", ""),
                metrics.get("npv", ""),
                metrics.get("irr", ""),
                metrics.get("roi", ""),
                metrics.get("payback_period", ""),
                risk.get("category", ""),
                risk.get("score", ""),
            ])
            content = csv_buffer.getvalue()
            return Response(
                content,
                mimetype="text/csv",
                headers={"Content-Disposition": f'attachment; filename="{filename}.csv"'},
            )

        if export_format == "pdf":
            pdf_buffer = BytesIO()
            doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
            styles = getSampleStyleSheet()
            elements = []
            elements.append(Paragraph(f"{project.name} - Feasibility Report", styles["Title"]))
            elements.append(Spacer(1, 16))
            elements.append(Paragraph(data.get("summary", ""), styles["BodyText"]))
            elements.append(Spacer(1, 16))

            table_data = [
                ["Metric", "Value"],
                ["NPV", str((data.get("metrics") or {}).get("npv", ""))],
                ["IRR", f"{(data.get('metrics') or {}).get('irr', '')}%"],
                ["ROI", f"{(data.get('metrics') or {}).get('roi', '')}%"],
                ["Payback", f"{(data.get('metrics') or {}).get('payback_period', '')} years"],
                ["Risk Category", str((data.get("risk") or {}).get("category", ""))],
                ["Risk Score", str((data.get("risk") or {}).get("score", ""))],
            ]
            table = Table(table_data)
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0b2545")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 1, colors.grey),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
            ]))
            elements.append(table)
            doc.build(elements)
            pdf_buffer.seek(0)
            return send_file(
                pdf_buffer,
                mimetype="application/pdf",
                as_attachment=True,
                download_name=f"{filename}.pdf",
            )

        return jsonify({"error": "Unsupported export format."}), 400

    @app.route("/api/health")
    def health_check():
        return {"status": "ok", "service": "feasibility-report-engine"}

    @app.route("/api/projects", methods=["GET"])
    def list_projects_api():
        projects = Project.query.order_by(Project.id.desc()).all()
        return jsonify({"projects": [project.to_dict() for project in projects]})

    @app.route("/api/reports/generate", methods=["POST"])
    def generate_report_api():
        payload = request.get_json(silent=True) or {}
        try:
            report = generate_project_report(payload)
            return jsonify(report), 200
        except ValueError as exc:
            return jsonify({"error": str(exc)}), 400

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
