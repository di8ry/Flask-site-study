from flask import Blueprint, current_app, render_template, abort, flash, redirect, request, url_for
from webapp.news.models import News, Comment
from webapp.news.utils.weather import get_weather_by_city
from webapp.news.forms import CommentForm
from flask_login import current_user, login_required
from webapp.db import db


blueprint = Blueprint('news', __name__)


@blueprint.route('/')
def index():
    title = 'Weather'
    rows = News.query.order_by(News.date.desc()).all()
    weather = get_weather_by_city(current_app.config['WEATHER_DEFAULT_CITY'])
    return render_template(
        'index.html',
        weather=weather,
        title=title,
        rows=rows
    )


@blueprint.route('/news/<int:news_id>')
def single_news(news_id):
    news = News.query.filter(News.id == news_id).first()
    if not news:
        abort(404)
    title = news.title
    form = CommentForm(news_id=news_id)
    return render_template(
        'single_news.html',
        title=title,
        news=news,
        form=form,
    )


@blueprint.route('/news/comment', methods=['POST'])
# @login_required
def add_comment():
    form = CommentForm()
    if form.validate_on_submit():
        if News.query.filter(News.id == form.news_id.data).first():
            comment = Comment(
                text=form.text.data,
                new_id=form.news_id.data,
                user_id=current_user.id,
            )
            db.session.add(comment)
            db.session.commit()
            flash('Комментарий добавлен')
            return redirect(request.referrer)
    error = list(form.errors.values())[0][0]
    flash(error)
    return redirect(url_for('news.index'))
