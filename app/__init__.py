# from flask import Flask, render_template # type: ignore
# from flask_socketio import SocketIO, emit # type: ignore

# from app.api import detections, artifacts, maintenance
# #app = Flask(__name__)
# app = Flask(__name__, template_folder="templates", static_folder="../static")
# app.config['SECRET_KEY'] = "@12345"
# socketio = SocketIO(app)

# @app.route('/')
# def index():
#     return render_template('index.html')
#     #return jsonify({'Message': 'Museum AI API is running!'})

# app.register_blueprint(detections.bp) # registering the blueprint
# app.register_blueprint(artifacts.bp)
# app.register_blueprint(maintenance.bp)

# if __name__ == '__main__':
#     socketio.run(app, debug=True)
