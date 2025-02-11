from wtforms import Form, StringField,SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf import FlaskForm

class RegisterForm(FlaskForm):
    username = StringField('Username', [DataRequired()], render_kw={"placeholder": "Username" , "class":"form-control"}) 
    email = StringField('Email', [DataRequired(), Email()], render_kw={"placeholder": "email" , "class":"form-control"})
    password = StringField('Password', [DataRequired()], render_kw={"placeholder": "password" , "class":"form-control"})
    confirm = StringField('Confirm Password', [DataRequired()], render_kw={"placeholder": "confirm password" , "class":"form-control"})
    submit = SubmitField('Submit', render_kw={"class":"btn btn-primary"})

    def validate_email(self,field):
        if field.data is not None and '@' not in field.data:
            raise ValidationError('Invalid Email')
    def validate_password(self,field):
        if len(field.data) < 8:
            raise ValidationError('Password must be at least 8 characters')

    def validate_confirm(self,field):
        if field.data != self.password.data:
            raise ValidationError('Password must match')

class LoginForm(FlaskForm):
    email = StringField('Email', [DataRequired(),Email()], render_kw={"placeholder": "email" , "class":"form-control"})
    password = StringField('Password', [DataRequired()], render_kw={"placeholder": "password" , "class":"form-control"})
    submit = SubmitField('Login', render_kw={"class":"btn btn-primary"})
