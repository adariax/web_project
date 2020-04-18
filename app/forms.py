from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField
from wtforms import DateTimeField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    nickname = StringField('Никнейм', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


class PostForm(FlaskForm):
    image = FileField(u'Image File')
    description = TextAreaField('Ввкдите текст публикации')
    datetime = DateTimeField('Дата публикации')
    submit = SubmitField('В очередь')
