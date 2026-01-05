from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class LocationForm(FlaskForm):
    city = StringField('Enter your city: ', validators=[DataRequired("Please enter a city")])
    america = BooleanField('Is this location in America?')
    state = StringField('Enter your state: ')
    country = StringField('Enter your country\'s ISO code: ', validators=[DataRequired("Please enter a valid country")])
    