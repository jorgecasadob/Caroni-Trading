from flask import Flask
from routes import routes
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)

app = Flask(__name__)

# Register the routes Blueprint
app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(debug=True)
