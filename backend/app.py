from flask import Flask, jsonify
from flask_cors import CORS
from database import init_db, get_db_connection
from routes.auth_routes import auth_bp
from routes.device_routes import device_bp
from routes.audit_routes import audit_bp


def create_app():
    app = Flask(__name__)
    CORS(app)

    init_db()

    app.register_blueprint(auth_bp)
    app.register_blueprint(device_bp)
    app.register_blueprint(audit_bp)

    @app.route("/")
    def home():
        return jsonify({
            "message": "SmartHome IoT Test Automation Backend is running",
            "status": "ok"
        })

    @app.route("/health")
    def health():
        try:
            conn = get_db_connection()
            conn.execute("SELECT 1")
            conn.close()

            return jsonify({
                "status": "ok",
                "db": True
            }), 200
        except Exception as e:
            return jsonify({
                "status": "error",
                "db": False,
                "error": str(e)
            }), 500

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, port=5000)