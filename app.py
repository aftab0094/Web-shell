from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class shell(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shell_output = db.Column(db.String)
    shell_input = db.Column(db.String)

    def __repr__(self):
        return 'test'

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)