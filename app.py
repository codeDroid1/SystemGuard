from src.config import app, db
from src import routes

def register_routes():
    app.register_blueprint(routes.homepage_bp)
    app.register_blueprint(routes.settings_bp)
    app.register_blueprint(routes.system_health_bp)
    app.register_blueprint(routes.cpu_info_bp)
    app.register_blueprint(routes.disk_info_bp)
    app.register_blueprint(routes.memory_info_bp)
    app.register_blueprint(routes.network_info_bp)
    app.register_blueprint(routes.speedtest_bp)
    app.register_blueprint(routes.process_bp)


if __name__ == "__main__":
    register_routes()
    
    # # Start the memory-consuming program in a separate thread
    # memory_thread = threading.Thread(target=memory_consuming_program, daemon=True)
    # memory_thread.start()
    
    # Run the Flask application
    app.run(host="0.0.0.0", port=5000, debug=True)
