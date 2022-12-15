from flask import Flask
from flask_login import LoginManager
from webapp.admin.views import blueprint as admin_blueprint
from webapp.news.views import blueprint as news_blueprint
from webapp.db import db
from webapp.user.views import blueprint as user_blueprint
from webapp.user.models import User
from flask_migrate import Migrate


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)

    app.register_blueprint(user_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(news_blueprint)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app


app = create_app()

# if __name__ == '__main__':
#     app.run(debug=True)
# export FLASK_APP=webapp && export FLASK_ENV=development && flask run
