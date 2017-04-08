import collections
import numpy as np
import chartkick
from flask import Flask, render_template, Blueprint
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import RadioField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_KEY'
Bootstrap(app)

ck = Blueprint('ck_page', __name__, static_folder=chartkick.js(),
               static_url_path='/static')
app.register_blueprint(ck, url_prefix='/ck')
app.jinja_env.add_extension("chartkick.ext.charts")


class ListForm(Form):
    body = TextAreaField('Введите список', validators=[DataRequired()])
    submit = SubmitField('Отправить')


class RadioForm(Form):
    example = RadioField(choices=[('gc', 'Google Charts'), ('cj', 'Chart.js'),
                         ('hc', 'Highcharts')])
    submit = SubmitField('Отправить')

default = [0, 0, 2, 0, 1, 3, 0, 1, 0, 1, 2, 1, 3, 0, 0, 2, 1, 3, 2, 2,
           1, 3, 3, 2, 0, 2, 4, 3, 2, 1, 2, 2, 2, 2, 3, 3, 1, 1, 1, 3,
           2, 1, 0, 1, 2, 1, 4, 4, 2, 3, 3, 6, 5, 2, 1, 2, 3, 2, 3, 1,
           1, 0, 1, 0, 4, 1, 0, 0, 2, 2, 4, 2, 1, 4, 3, 0, 2, 0, 2, 0,
           3, 1]

defaultl = np.array(default)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500


@app.route("/", methods=['GET', 'POST'])
def chart():
    radio_form = RadioForm()
    list_form = ListForm()
    counter = collections.Counter(defaultl)
    data = dict(counter)
    if radio_form.validate_on_submit():
        if radio_form.example.data == 'gc':
            return render_template('googlecharts.html', data=data,
                                   radio_form=radio_form, list_form=list_form)
        elif radio_form.example.data == 'cj':
            return render_template('chartjs.html', data=data,
                                   radio_form=radio_form, list_form=list_form)
        elif radio_form.example.data == 'hc':
            return render_template('highcharts.html', data=data,
                                   radio_form=radio_form, list_form=list_form)
    else:
        print(radio_form.errors)

    if list_form.validate_on_submit():
        data = list_form.body.data
        a = [int(s) for s in list_form.body.data.split(",")]
        an = np.array(a)
        print(an)
        counter = collections.Counter(an)
        data = dict(counter)
    return render_template('highcharts.html', data=data, radio_form=radio_form,
                           list_form=list_form)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
