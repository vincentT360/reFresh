from flask import Flask

app = Flask(__name__)


from flaskdriver.main.routes import main
app.register_blueprint(main)