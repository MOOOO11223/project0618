from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    UserID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(50), unique=True, nullable=False)
    Password = db.Column(db.String(255), nullable=False)
    UserType = db.Column(db.String(10), nullable=False)

class TrainingDataset(db.Model):
    __tablename__ = 'trainingdatasets'
    DatasetID = db.Column(db.Integer, primary_key=True)
    DatasetName = db.Column(db.String(50), nullable=False)
    TeacherID = db.Column(db.Integer, db.ForeignKey('users.UserID'), nullable=False)
    TrainingDataPath = db.Column(db.String(255), nullable=False)
    ValidationDataPath = db.Column(db.String(255), nullable=False)
    CreatedAt = db.Column(db.DateTime, default=datetime.utcnow)

class Model(db.Model):
    __tablename__ = 'models'
    ModelID = db.Column(db.Integer, primary_key=True)
    ModelName = db.Column(db.String(50), nullable=False)
    StudentID = db.Column(db.Integer, db.ForeignKey('users.UserID'), nullable=False)
    DatasetID = db.Column(db.Integer, db.ForeignKey('trainingdatasets.DatasetID'), nullable=False)
    ModelPath = db.Column(db.String(255), nullable=False)
    Accuracy = db.Column(db.Float)
    CreatedAt = db.Column(db.DateTime, default=datetime.utcnow)

class Score(db.Model):
    __tablename__ = 'scores'
    ScoreID = db.Column(db.Integer, primary_key=True)
    StudentID = db.Column(db.Integer, db.ForeignKey('users.UserID'), nullable=False)
    ModelID = db.Column(db.Integer, db.ForeignKey('models.ModelID'), nullable=False)
    Score = db.Column(db.Float)
    CreatedAt = db.Column(db.DateTime, default=datetime.utcnow)