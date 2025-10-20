from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

# class NewModel(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     firstCol = db.Column(db.String(100))


class DemoData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    demoText = db.Column(db.String(100))
    demoNumber = db.Column(db.Integer)
    demoBool = db.Column(db.Boolean)
    created = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated = db.Column(db.DateTime, default=datetime.now(timezone.utc))