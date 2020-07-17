from flask import Flask
from quickbooks.views import QUICKBOOKS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
SQLAlchemy(app)

app.register_blueprint(QUICKBOOKS)

@app.route('/healthz')
def healthz():
    return 'ok'

if __name__ == '__main__':
    app.run(debug=True)
