from flask import Flask, jsonify, request, render_template, redirect, url_for

from config.database import get_database_uri
from database.models import db, init_db, Project, Report
from src.engine import generate_project_report


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = get_database_uri()
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JSON_SORT_KEYS"] = False
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
    app.config["TEMPLATES_AUTO_RELOAD"] = True

    init_db(app)
