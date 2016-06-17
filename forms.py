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


class NewCollectionForm(Form):
    input_error = ('Invalid input. Please remove special characters and '
                   'try again.')

    path_input_error = ('Invalid input. The only allowed characters for '
                        'path are letters and numbers.')
    name = (
        StringField('Name: ',
                    validators=[DataRequired(),
                                Regexp(regex=r'^[a-zA-Z0-9_,\-_();:\' ]+$',
                                       message=input_error)
                                ]))
    path = StringField('Path: ',
                        validators = [DataRequired(),
                                     Regexp(regex=r'^[a-zA-Z0-9]+$',
                                            message=path_input_error)
                                     ])
    description = (
        TextAreaField('Description: ',
                      validators=[DataRequired(),
                                 Regexp(
                                    regex=r'^[a-zA-Z0-9_.,\-_();:\'?! ]+$',
                                    message=input_error)
                                 ]))


class EditCategoryForm(Form):
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

class NewCategoryForm(Form):
    input_error = ('Invalid input. Please remove special characters and '
                   'try again.')

    path_input_error = ('Invalid input. The only allowed characters for '
                        'path are letters and numbers.')
    name = (
        StringField('Name: ',
                    validators=[DataRequired(),
                                Regexp(regex=r'^[a-zA-Z0-9_,\-_();:\' ]+$',
                                       message=input_error)
                                ]))
    path = StringField('Path: ',
                        validators = [DataRequired(),
                                     Regexp(regex=r'^[a-zA-Z0-9]+$',
                                            message=path_input_error)
                                     ])
    description = (
        TextAreaField('Description: ',
                      validators=[DataRequired(),
                                 Regexp(
                                    regex=r'^[a-zA-Z0-9_.,\-_();:\'?! ]+$',
                                    message=input_error)
                                 ]))