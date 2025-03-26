from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, FloatField, FileField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from models import User

class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    terms_agree = BooleanField('I agree to the Terms of Service and Privacy Policy', validators=[DataRequired()])
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is already taken. Please choose a different one.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already registered. Please use a different one.')

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[Length(max=20)])
    interest = SelectField('Interest', choices=[
        ('General Inquiry', 'General Inquiry'),
        ('Spiritual', 'Spiritual Journey'),
        ('Cultural', 'Cultural Experience'),
        ('Adventure', 'Adventure Trip'),
        ('Wellness', 'Wellness Retreat'),
        ('Heritage', 'Heritage Tour')
    ])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send Message')

class PackageForm(FlaskForm):
    name = StringField('Package Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    price = FloatField('Price (₹)', validators=[DataRequired()])
    duration = StringField('Duration', validators=[DataRequired(), Length(max=50)])
    category = SelectField('Category', choices=[
        ('Spiritual', 'Spiritual'),
        ('Cultural', 'Cultural'),
        ('Adventure', 'Adventure'),
        ('Wellness', 'Wellness'),
        ('Heritage', 'Heritage')
    ], validators=[DataRequired()])
    location_id = SelectField('Location', coerce=int, validators=[DataRequired()])
    featured_image = StringField('Featured Image URL')
    submit = SubmitField('Save Package')

class LocationForm(FlaskForm):
    name = StringField('Location Name', validators=[DataRequired(), Length(max=100)])
    region = SelectField('Region', choices=[
        ('North India', 'North India'),
        ('South India', 'South India'),
        ('East India', 'East India'),
        ('West India', 'West India'),
        ('Central India', 'Central India'),
        ('Northeast India', 'Northeast India')
    ], validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    latitude = FloatField('Latitude', validators=[DataRequired()])
    longitude = FloatField('Longitude', validators=[DataRequired()])
    featured_image = StringField('Featured Image URL')
    submit = SubmitField('Save Location')

class ImageUploadForm(FlaskForm):
    image = FileField('Select Image', validators=[DataRequired()])
    category = SelectField('Image Category', choices=[
        ('Location Image', 'Location Image'),
        ('Package Image', 'Package Image'),
        ('Banner Image', 'Banner Image'),
        ('Other', 'Other')
    ], validators=[DataRequired()])
    description = StringField('Image Usage/Description')
    submit = SubmitField('Upload Image')
