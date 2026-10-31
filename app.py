from flask import Flask, jsonify, request

from config.database import get_database_uri
from database.models import db, init_db
from src.engine import generate_project_report


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = get_database_uri()
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JSON_SORT_KEYS"] = False

    db.init_app(app)
    init_db(app)

    @app.route("/")
    def index():
        return {
            "status": "ok",
            "service": "feasibility-report-engine",
            "message": "API ready. Use /api/health or POST /api/reports/generate.",
        }

    @app.route("/api/health")
    def health_check():
        return {"status": "ok", "service": "feasibility-report-engine"}

    @app.route("/api/reports/generate", methods=["POST"])
    def generate_report():
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
