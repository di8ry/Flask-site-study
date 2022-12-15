from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import DataRequired, ValidationError
from webapp.news.models import News


class CommentForm(FlaskForm):
    news_id = HiddenField('ID news', validators=[DataRequired()])
    text = StringField(
        'Ваш комментарий',
        validators=[DataRequired()],
        render_kw={'class': 'form-control'},
        )
    submit = SubmitField('Отправить', render_kw={'class': 'btn btn-success'})

    def validate_news_id(self, news_id):
        if not News.query.get(news_id.data):
            raise ValidationError('Новость удалена!')


class SearchForm(FlaskForm):
    searched = StringField('searched', validators=[DataRequired()])
    submit = SubmitField('submit')

