from flask import Flask, render_template
from config import Config
from extensions import db, jwt
from routes.auth import auth_bp
from routes.device import device_bp
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(device_bp)

    @app.route('/')
    def index():
        return render_template('login.html')

    return app


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        from models.user import User  # 确保导入模型
        db.create_all()

    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
