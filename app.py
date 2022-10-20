from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_email import send_email

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/Body_collector'
db = SQLAlchemy(app)


class Data(db.Model):
    __tablename__ = "data"
    id = db.Column(db.Integer, primary_key=True)
    email_ = db.Column(db.String(120), unique=True)
    height_ = db.Column(db.Integer)
    weight_ = db.Column(db.Integer)
    BMI_ = db.Column(db.Float)

    def __init__(self, email_, height_, weight_, BMI_):
        self.email_ = email_
        self.height_ = height_
        self.weight_ = weight_
        self.BMI_ = BMI_


with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return render_template("front.html")


@app.route('/success', methods=['POST'])
def success():
    if request.method == 'POST':
        email = request.form["email_name"]
        height = request.form["height_name"]
        weight = request.form["weight_name"]

        BMI_index = round(float(weight) / pow(float(height) / 100, 2), 2)

        send_email(email, BMI_index)

    if db.session.query(Data).filter(Data.email_ == email).count() == 0:
        data = Data(email, height, weight, BMI_index)
        db.session.add(data)
        db.session.commit()
        return render_template("successful.html")
    else:
        data = Data(email, height, weight, BMI_index)
        db.session.query(Data).filter(Data.email_ == email).update({"weight_": weight})
        db.session.query(Data).filter(Data.email_ == email).update({"height_": height})
        db.session.query(Data).filter(Data.email_ == email).update({"BMI_": BMI_index})
        db.session.commit()
    return render_template("front.html", text="You have uploaded before, we will renew your new data!")


if __name__ == '__main__':
    debug = True
    app.run()
