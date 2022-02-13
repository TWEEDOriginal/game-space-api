import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_swagger_ui import get_swaggerui_blueprint

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

db = SQLAlchemy()


def create_app(database=db):
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    database.init_app(app)

    """
    Swagger UI configurations
    """
    SWAGGER_URL = "/docs"
    API_URL = "/static/swagger.json"
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={"app_name": "Get best value for games application"},
    )

    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    try:
        from blueprints.api_views import main as api_endpoints
        from blueprints.error_views import miscellanous
    except ImportError:
        from .blueprints.api_views import main as api_endpoints
        from .blueprints.error_views import miscellanous

    app.register_blueprint(api_endpoints)
    app.register_blueprint(miscellanous)

    return app


if __name__ == "__main__":
    app = create_app(database=db)
    app.run(port=5500)
