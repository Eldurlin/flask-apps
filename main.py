from flask.views import MethodView
from wtforms import Form, StringField, SubmitField
from flask import Flask, render_template, request
from flatmates_bill import flat
from calories import calorie, temperature


app = Flask(__name__)


class IndexPage(MethodView):  
    def get(self):
        
        return render_template('index_page.html')


class BillFormPage(MethodView):
    def get(self):
        billform = BillForm()

        return render_template(
            'bill_form_page.html',
            billform=billform)

    def post(self):
        billform = BillForm(request.form)

        the_bill = flat.Bill(
            float(billform.amount.data),
            billform.period.data)

        flatmate1 = flat.Flatmate(
            billform.name1.data,
            float(billform.days_in_house1.data))

        flatmate2 = flat.Flatmate(
            billform.name2.data,
            float(billform.days_in_house2.data))

        return render_template(
            'bill_form_page.html',
            billform=billform,
            result=True,
            name1=flatmate1.name,
            amount1=flatmate1.pays(the_bill, flatmate2),
            name2=flatmate2.name,
            amount2=flatmate2.pays(the_bill, flatmate1))        


class BillForm(Form):
    amount = StringField(
        'Bill amount: ',
        default='120')

    period = StringField(
        'Bill period: ',
        default='May 2021')

    name1 = StringField(
        'Name: ',
        default='Hansel')

    days_in_house1 = StringField(
        'Days in the house: ',
        default=18)

    name2 = StringField(
        'Name: ',
        default='Gretel')

    days_in_house2 = StringField(
        'Days in the house: ',
        default=16)

    button = SubmitField('Calculate')


class CaloriesFormPage(MethodView):
    def get(self):
        caloriesform = CaloriesForm()

        return render_template(
            'calories_form_page.html',
            caloriesform=caloriesform)

    def post(self):
        caloriesform = CaloriesForm(request.form)

        the_temperature = temperature.Temperature(
            country=caloriesform.country.data,
            city=caloriesform.city.data).get()

        the_calories = calorie.Calorie(
            float(caloriesform.weight.data),
            float(caloriesform.height.data),
            float(caloriesform.age.data),
            temperature=the_temperature)

        calories = the_calories.calculate()

        return render_template(
            'calories_form_page.html',
            caloriesform=caloriesform,
            result=True,
            temperature=the_temperature,
            calories=calories)


class CaloriesForm(Form):
    weight = StringField(
        'Weight: ',
        default=70)

    height = StringField(
        'Height: ',
        default=175)

    age = StringField(
        'Age: ',
        default=25)

    country = StringField(
        'Country: ',
        default='Poland')

    city = StringField(
        'City: ',
        default='Warsaw')

    button = SubmitField(
        'Calculate')


app.add_url_rule(
    '/',
    view_func=IndexPage.as_view('index_page'))

app.add_url_rule(
    '/bill_form_page',
    view_func=BillFormPage.as_view('bill_form_page'))
    
app.add_url_rule(
    '/calories_form_page',
    view_func=CaloriesFormPage.as_view('calories_form_page'))

app.run(debug=True)