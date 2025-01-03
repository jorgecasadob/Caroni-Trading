<<<<<<< HEAD
from flask import Flask
from flask import Flask
from routes import routes

app = Flask(__name__)

# Register the routes Blueprint
app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(debug=True)

=======
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify(message="Welcome to Caroni Trading API!")

if __name__ == '__main__':
    app.run(debug=True)
>>>>>>> 6c9dcf26be9af9b94a17bac3d3a6289e50428916
