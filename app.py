from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from sqlalchemy import func

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


@app.route('/', methods=["POST", "GET"])
def home():
    if request.method == "POST" and request.form["id"]:
        target = request.form["id"]
        db.session.query(Tasks).filter(Tasks.id == target).delete()
        db.session.commit()
    return render_template("index.html", tasks=Tasks.query.all())


@app.route('/new', methods=["POST", "GET"])
def new_task():
    if request.method == "POST":
        errors = []
        taskname = request.form["title"]
        notes = request.form["notes"]
        if len(taskname) > 32 or len(taskname) < 1:
            errors.append("Task name must be between 1 and 32 characters.")
        if len(notes) > 256:
            errors.append("Notes must not exceed 256 characters.")
        if Tasks.query.count() >= 25:
            errors.append("You cannot have more than 25 notes only because I said so. Please don't flood the database.")
        if len(errors) > 0:
            title = "New Task"
            return render_template("new_task.html", title=title, errors=errors)
        task = Tasks(title=taskname, notes=notes)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for("home"))
    else:
        title = "New Task"
        return render_template("new_task.html", title=title)


@app.route('/about')
def about():
    title = "About"
    return render_template("about.html", title=title)


if __name__ == '__main__':
    app.run()


class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), unique=False, nullable=False)
    notes = db.Column(db.String(256), unique=False, nullable=True)
    created = db.Column(db.DateTime(), default=func.now())

    def __repr__(self):
        return f"Task: ID[{self.id}], Title[{self.title}], CreatedOn[{self.created}]"



