from flask import Flask

app = Flask(__name__)


@app.route('/helloworld')
def HelloWorld():
	'''
	hello world controller
	'''
	return 'hello world'


if __name__ == '__main__':
  app.secret_key = 'ItemCatalogUdacity'
  app.debug = True
  app.run(host = '0.0.0.0', port = 8000)



