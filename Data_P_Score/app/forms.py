from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired

class BusinessForm(Form):
    business_name = StringField('business_name', validators=[DataRequired()])
    owner = StringField('owner', validators=[DataRequired()])
    business_type = StringField('business_type', validators=[DataRequired()])
    location = StringField('location', validators=[DataRequired()])