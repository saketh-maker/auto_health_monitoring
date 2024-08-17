from flask import Flask, render_template, redirect, url_for, request, session
from models import db, User, Report
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'your_secret_key'

db.init_app(app)
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/upload_report', methods=['GET', 'POST'])
def upload_report():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        patient_name = request.form['patient_name']
        diagnosis = request.form['diagnosis']
        report = Report(patient_name=patient_name, diagnosis=diagnosis, user_id=session['user_id'])
        db.session.add(report)
        db.session.commit()
        return redirect(url_for('view_reports'))
    return render_template('upload_report.html')

@app.route('/view_reports')
def view_reports():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    reports = Report.query.filter_by(user_id=session['user_id']).all()
    return render_template('view_reports.html', reports=reports)

if __name__ == '__main__':
    app.run(debug=True)
