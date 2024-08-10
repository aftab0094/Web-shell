from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
import subprocess as sp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class shell(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shell_output = db.Column(db.String)
    shell_input = db.Column(db.String)

    def __repr__(self):
        return f'<Command {self.id}>'

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method =='POST':
        command_content = request.form['shell_show']
        new_command = shell(shell_input=command_content)

        try:
            command_output = sp.check_output(command_content, shell=True, text=True)
        except sp.CalledProcessError:
            command_output = 'command not found'
        except Exception as e:
            command_output = f'Error: {str(e)}'
        new_command.shell_output = command_output

        print(f'{command_content}\n{command_output}')

        try:
            db.session.add(new_command)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            raise Exception(e)
    else:
        commands = shell.query.all()
        print(commands)
        for command in commands:
            print(command)
            print(command.shell_input)
            print(command.shell_output)
        return render_template('index.html', commands=commands)

if __name__ == "__main__":
    app.run(debug=True)