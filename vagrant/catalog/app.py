from flask import Flask
from routes import *

app = Flask(__name__)
app.secret_key = 'ItemCatalogUdacity'

app.register_blueprint(routes)
if __name__ == '__main__':
  app.debug = True
  app.run(host = '0.0.0.0', port = 5000)