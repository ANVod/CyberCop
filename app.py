import openai
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Конфигурация базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Конфигурация ключа API OpenAI
openai.api_key = 'your-openai-api-key'

# Модель базы данных
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

# Инициализация базы данных
db.create_all()

# Маршруты
@app.route('/')
def index():
    return render_template('report.html')

@app.route('/submit', methods=['POST'])
def submit():
    crime_type = request.form['crime_type']
    description = request.form['description']
    date_time = request.form['date_time']
    evidence = request.form.get('evidence', None)  # Обработка необязательного поля доказательств

    report = CrimeReport(crime_type, description, date_time, evidence)
    db.session.add(report)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.json['message']
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=user_input,
        max_tokens=150
    )
    return jsonify({"response": response.choices[0].text.strip()})

# Запуск приложения
if __name__ == '__main__':
    app.run(debug=True)