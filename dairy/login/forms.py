from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, RadioField, PasswordField,BooleanField, FileField
from wtforms.validators import DataRequired,Length,Email,EqualTo
from flask_wtf.file import FileAllowed


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=5, max=20)])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    user_type = RadioField("User Type", validators=[DataRequired()], choices=[('Admin', 'Admin'),
                                                                               ('Farmer', 'Farmer')])
    firstname = StringField("First Name", validators=[DataRequired()])
    lastname = StringField("Last Name", validators=[DataRequired()])
    farmname = StringField("Farm Name", validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired()])
    mobilenum = StringField("Telephone",validators=[DataRequired()])
    submit = SubmitField("Create Account")
    
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember")
    submit = SubmitField("Login")
    
    
    
class AccountForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=5, max=20)])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    user_type = RadioField("User Type", validators=[DataRequired()], choices=[('Admin', 'Admin'),
                                                                               ('Farmer', 'Farmer')])
    firstname = StringField("First Name", validators=[DataRequired()])
    lastname = StringField("Last Name", validators=[DataRequired()])
    farmname = StringField("Farm Name", validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired()])
    mobilenum = StringField("Telephone",validators=[DataRequired()])
    picture = FileField("Update your Image", validators=[FileAllowed(['jpeg', 'png', 'jpg'])])
    submit = SubmitField("Update Account")    