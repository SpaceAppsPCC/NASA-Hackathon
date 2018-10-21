from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
@app.route('/home/')
def home():
    # Connecting to a template (html file)
	return render_template('home.html')

@app.route('/puppy/<name>')
def pup_name(name):
	return render_template('puppy.html',name=name)

@app.route('/about/')
def about():
  	return render_template('about.html')


if __name__ == '__main__':
	app.run(debug=True)
