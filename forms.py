from flask_wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import (DataRequired, Regexp, ValidationError,
                                URL, Length)


class EditCollectionForm(Form):
    input_error = ('Invalid input. Please remove special characters and '
                   'try again.')

    name = (
        StringField('Name: ',
                    validators=[DataRequired(),
                                Length(min=2, max=20),
                                Regexp(regex=r'^[a-zA-Z0-9_,\-_();:\' ]+$',
                                       message=input_error)
                                ]))
    description = (
        TextAreaField('Description: ',
                      validators=[DataRequired(),
                                  Length(min=2, max=130),
                                 Regexp(
                                    regex=r'^[a-zA-Z0-9_.,\-_();:\'?! ]+$',
                                    message=input_error)
                                 ]))

class NewCollectionForm(Form):
    input_error = ('Invalid input. Please remove special characters and '
                   'try again.')

    path_input_error = ('Invalid input. The only allowed characters for '
                        'path are letters and numbers.')

    path_desc = ('Path should be a single word (or multiple words separated '
                 'by hyphens) that will be used in the link to the '
                 'collection\'s page.')
    name = (
        StringField('Name: ',
                    validators=[DataRequired(),
                                Length(min=2, max=20),
                                Regexp(regex=r'^[a-zA-Z0-9_,\-_();:\' ]+$',
                                       message=input_error)
                                ]))
    path = StringField('Path: ',
                        description=path_desc,
                        validators = [DataRequired(),
                                      Length(min=2, max=20),
                                     Regexp(regex=r'^[a-zA-Z0-9\-]+$',
                                            message=path_input_error +
                                                    ' ' + path_desc)
                                     ])
    description = (
        TextAreaField('Description: ',
                      validators=[DataRequired(),
                                  Length(min=2, max=130),
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
                                Length(min=2, max=20),
                                Regexp(regex=r'^[a-zA-Z0-9_,\-_();:\' ]+$',
                                       message=input_error)
                                ]))
    description = (
        TextAreaField('Description: ',
                      validators=[DataRequired(),
                                  Length(min=2, max=200),
                                 Regexp(
                                    regex=r'^[a-zA-Z0-9_.,\-_();:\'?! ]+$',
                                    message=input_error)
                                 ]))

class NewCategoryForm(Form):
    input_error = ('Invalid input. Please remove special characters and '
                   'try again.')

    path_input_error = ('Invalid input. The only allowed characters for '
                        'path are letters and numbers.')

    path_desc = ('Path should be a single word (or multiple words separated '
                 'by hyphens) that will be used in the link to the '
                 'collection\'s page.')
    name = (
        StringField('Name: ',
                    validators=[DataRequired(),
                                Length(min=2, max=20),
                                Regexp(regex=r'^[a-zA-Z0-9_,\-_();:\' ]+$',
                                       message=input_error)
                                ]))
    path = StringField('Path: ',
                        description=path_desc,
                        validators = [DataRequired(),
                                      Length(min=2, max=20),
                                      Regexp(regex=r'^[a-zA-Z0-9]+$',
                                            message=path_input_error + ' ' +
                                                    path_desc)
                                     ])
    description = (
        TextAreaField('Description: ',
                      validators=[DataRequired(),
                                  Length(min=2, max=200),
                                  Regexp(
                                    regex=r'^[a-zA-Z0-9_.,\-_();:\'?! ]+$',
                                    message=input_error)
                                 ]))


class EditLinkForm(Form):
    input_error = ('Invalid input. Please remove special characters and '
                   'try again.')

    url_input_error = ('Invalid URL entered.')

    url_desc = 'The URL should be a link formatted like http://www.example.com'

    name = (
        StringField('Name: ',
                    validators=[DataRequired(),
                                Length(min=2, max=20),
                                Regexp(regex=r'^[a-zA-Z0-9_,\-_();:\' ]+$',
                                       message=input_error)
                                ]))
    url = StringField('URL: ',
                        description = url_desc,
                        validators = [DataRequired(),
                                      Length(min=10, max=200),
                                      URL(require_tld=True,
                                          message=url_input_error + ' ' +
                                                  url_desc)
                                     ])
    description = (
        TextAreaField('Description: ',
                      validators=[DataRequired(),
                                  Length(min=2, max=200),
                                  Regexp(
                                    regex=r'^[a-zA-Z0-9_.,\-_();:\'?! ]+$',
                                    message=input_error)
                                 ]))
class NewLinkForm(Form):
    input_error = ('Invalid input. Please remove special characters and '
                   'try again.')

    url_input_error = ('Invalid URL entered.')

    url_desc = 'The URL should be a link formatted like http://www.example.com'

    name = (
        StringField('Name: ',
                    validators=[DataRequired(),
                                Length(min=2, max=20),
                                Regexp(regex=r'^[a-zA-Z0-9_,\-_();:\' ]+$',
                                       message=input_error)
                                ]))
    url = StringField('URL: ',
                        description = url_desc,
                        validators = [DataRequired(),
                                      Length(min=2, max=200),
                                      URL(require_tld=True,
                                          message=url_input_error + ' ' +
                                                  url_desc)
                                     ])
    description = (
        TextAreaField('Description: ',
                      validators=[DataRequired(),
                                  Length(min=2, max=200),
                                 Regexp(
                                    regex=r'^[a-zA-Z0-9_.,\-_();:\'?! ]+$',
                                    message=input_error)
                                 ]))