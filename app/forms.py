from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,EmailField,PasswordField,FloatField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField


class EditForm(FlaskForm):
    rating = FloatField('Your Rating Out: ', validators=[DataRequired()])
    review = StringField('Your Review: ', validators=[DataRequired()])
    submit = SubmitField('Done')

class DeleteForm(FlaskForm):
    submit = SubmitField("Delete")

class AddForm(FlaskForm):
    add = StringField('Movie title: ', validators=[DataRequired()])
    submit = SubmitField("Add Movie")
    

class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")



class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let Me In!")