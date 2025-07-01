from flask import Flask
from get_balance import get_bp
from post_balance import post_bp

app = Flask(__name__)

app.register_blueprint(get_bp)
app.register_blueprint(post_bp)

if __name__ == '__main__':
    app.run(debug=True)
