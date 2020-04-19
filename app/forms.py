from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, DateTimeField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    nickname = StringField('Никнейм', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


class PostForm(FlaskForm):
    image = FileField(u'Image File', validators=[FileRequired(), FileAllowed(['jpg', 'png'])])
    description = TextAreaField('Введите текст публикации')
    datetime = DateTimeField('Дата публикации')
    from_group = BooleanField('От имени группы')
    signed = BooleanField('Подпись автора')
    submit = SubmitField('В очередь')
