from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_wtf.file import FileField

class UploadFile(FlaskForm):
    file = FileField("file", validators=[DataRequired()])
    submit = SubmitField("Pridaj súbor")

class CreateDirectory(FlaskForm):
    directoryName = StringField("Zadajte názov priečinka ktorý chcete vytvoriť", validators=[DataRequired()])
    submit = SubmitField("Vytvorte Priečinok")

class ChangeDirectory(FlaskForm):
    directoryName = StringField("Názov priečinka", validators=[DataRequired()])
    submit = SubmitField("Zmen priečinok")