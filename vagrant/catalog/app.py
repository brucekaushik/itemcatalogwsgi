from flask import Flask
from routes import *

app = Flask(__name__)

app.register_blueprint(routes)

if __name__ == '__main__':
  app.secret_key = 'ItemCatalogUdacity'
  app.debug = True
  app.run(host = '0.0.0.0', port = 8000)