from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# class NewModel(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     firstCol = db.Column(db.String(100))