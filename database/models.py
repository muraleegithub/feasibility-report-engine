from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, default="")
    currency = db.Column(db.String(10), default="USD")
    investment = db.Column(db.Float, default=0.0)
    annual_revenue = db.Column(db.Float, default=0.0)
    annual_cost = db.Column(db.Float, default=0.0)
    growth_rate = db.Column(db.Float, default=0.0)
    years = db.Column(db.Integer, default=5)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    reports = db.relationship("Report", backref="project", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "currency": self.currency,
            "investment": self.investment,
            "annual_revenue": self.annual_revenue,
            "annual_cost": self.annual_cost,
            "growth_rate": self.growth_rate,
            "years": self.years,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Report(db.Model):
    __tablename__ = "reports"

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    generated_at = db.Column(db.DateTime, server_default=db.func.now())
    summary = db.Column(db.Text, default="")
    metrics = db.Column(db.JSON, default=dict)
    risk = db.Column(db.JSON, default=dict)
    strategic = db.Column(db.JSON, default=dict)

    def to_dict(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "generated_at": self.generated_at.isoformat() if self.generated_at else None,
            "summary": self.summary,
            "metrics": self.metrics,
            "risk": self.risk,
            "strategic": self.strategic,
        }


def init_db(app=None):
    if app is not None:
        db.init_app(app)

    app_obj = app
    if app_obj is None:
        from flask import current_app
        app_obj = current_app._get_current_object()

    with app_obj.app_context():
        db.create_all()
