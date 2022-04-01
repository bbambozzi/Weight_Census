from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_email import send_email
from sqlalchemy import func
import pytest

# We'll be importing flask and SQLAlchemy from within the local environment.


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://general_test:postgres123@localhost/flask_website'
# We're connecting to the database utilizing SQLAlchemy, we'll be interacting with our database.
# We also input the username, password and name of the database.
db = SQLAlchemy(app)


# We initialize Flask and the postgres-based database.

class Data(db.Model):
    __tablename__ = "data"
    id = db.Column(db.Integer, primary_key=True)
    local_email = db.Column(db.String(120), unique=True)
    local_weight = db.Column(db.Integer)

    # We create the three columns which will store user information.

    def __init__(self, local_email, local_weight):
        self.local_email = local_email
        self.local_weight = local_weight


@app.route("/")
def index():
    return render_template("index.html")


# Simple display of the html index page.


@app.route("/success", methods=['POST'])
def success():
    if request.method == 'POST':
        user_email = request.form["email_name"]
        user_weight = request.form["user_weight"]
        data = Data(user_email, user_weight)  # Grab the user data and use the Data object.
        print(user_email, user_weight)
        if db.session.query(Data).filter(Data.local_email == user_email).count() == 0:  # If the user is new...
            db.session.add(data)
            db.session.commit()  # We add the data.
            average_weight = db.session.query(func.avg(Data.local_weight)).scalar()  # We calculate the AVG (SQLAlchemy)
            average_weight = round(average_weight, 2)
            total_queries = db.session.query(Data.local_weight).count()  # We calculate the total amount of queries
            send_email(user_email, user_weight, average_weight, total_queries)  # And we send it off!
            return render_template("success.html")  # Redirect to another html for a prettier confirmation message.
        return render_template("index.html", text="We already have this E-Mail in our database!")


# Redirect to the "success" html page.


if __name__ == "__main__":
    app.debug = True
    app.run()

# We can use "from app import db" and "db.create_all()" from the python console to generate the tables if needed.

# Unit tests and integration tests
