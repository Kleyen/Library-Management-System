from flask import Flask
from app.extensions import db, migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    migrate.init_app(app, db)

    from app.models.book import Book
    from app.models.member import Member
    from app.models.loan import Loan

    from app.routes.main import main
    from app.routes.books import books
    from app.routes.members import members
    from app.routes.loans import loans

    app.register_blueprint(main)
    app.register_blueprint(books)
    app.register_blueprint(members)
    app.register_blueprint(loans)

    from flask import render_template

    @app.errorhandler(404)
    def not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('errors/500.html'), 500

    return app