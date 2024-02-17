from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///polzovatel.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    tasks = db.relationship('Task', backref='user', lazy=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        task_description = request.form['task']
        user = User(username=username, email=email)
        task = Task(description=task_description, user=user)
        db.session.add(user)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('user_list'))
    return render_template('register.html')

@app.route('/user_list')
def user_list():
    users = User.query.all()
    return render_template('user_list.html', users=users)

@app.route('/update_task/<int:user_id>/<int:task_id>', methods=['POST'])
def update_task(user_id, task_id):
    new_task_description = request.form['task']
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if task:
        task.description = new_task_description
        db.session.commit()
    return redirect(url_for('user_list'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)