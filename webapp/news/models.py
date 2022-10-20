from webapp.db import db
from datetime import datetime
from sqlalchemy.orm import relationship
from wtforms.validators import ValidationError


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False, unique=True)
    date = db.Column(db.DateTime, nullable=False)
    text = db.Column(db.Text, nullable=True)

    def comments_count(self):
        return Comment.query.filter(Comment.news_id == self.id).count()

    def __repr__(self):
        return f'News {self.id}: {self.title}'


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, default=datetime.now())

    news_id = db.Column(
        db.Integer,
        db.ForeignKey('news.id', ondelete='CASCADE'),
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', ondelete='CASCADE'),
    )

    news = relationship('News', backref='comments')
    user = relationship('User', backref='comments')

    def __repr__(self):
        return f'Comment {self.id}: {self.text} от {self.user_id} к новости {self.news_id}'
