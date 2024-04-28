from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class CrimeReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    crime_type = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_time = db.Column(db.String(80), nullable=False)
    evidence = db.Column(db.String(300))

    def __init__(self, crime_type, description, date_time, evidence=None):
        self.crime_type = crime_type
        self.description = description
        self.date_time = date_time
        self.evidence = evidence


db.create_all()


@app.route('/')
def index():
    return render_template('report.html')


@app.route('/submit', methods=['POST'])
def submit():
    crime_type = request.form['crime_type']
    description = request.form['description']
    date_time = request.form['date_time']
    evidence = request.form['evidence']

    report = CrimeReport(crime_type, description, date_time, evidence)
    db.session.add(report)
    db.session.commit()

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)