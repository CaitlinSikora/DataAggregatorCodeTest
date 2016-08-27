from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired

class CompanyForm(Form):
    company = StringField('company', validators=[DataRequired()])
    owner_first = StringField('owner_first', validators=[DataRequired()])
    owner_last = StringField('owner_last', validators=[DataRequired()])
    location = StringField('location', validators=[DataRequired()])