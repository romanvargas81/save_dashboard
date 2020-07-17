from wtforms import Form
from wtforms.fields.html5 import DateField, DecimalField
from wtforms.validators import InputRequired

class QuickBooksForm(Form):
    period = DateField('period', [InputRequired()])
    wisetack_junior_position = DecimalField('wisetack_junior_position', validators=[InputRequired()])
    lighter_junior_position = DecimalField('lighter_junior_position',  validators=[InputRequired()])
