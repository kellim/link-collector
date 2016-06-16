from flask_wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import (DataRequired, Regexp, ValidationError)

class EditCollectionForm(Form):
    input_error = ('Invalid input. Please remove special characters and '
                   'try again.')

    name = (
        StringField('Name: ',
                    validators=[DataRequired(),
                                Regexp(regex=r'^[a-zA-Z0-9_,\-_();:\' ]+$',
                                       message=input_error)
                                ]))
    description = (
        TextAreaField('Description: ',
                      validators=[DataRequired(),
                                 Regexp(
                                    regex=r'^[a-zA-Z0-9_.,\-_();:\'?! ]+$',
                                    message=input_error)
                                 ]))