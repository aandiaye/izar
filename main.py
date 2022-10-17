from flask import Flask, render_template


app = Flask(__name__)
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/index')
def home():
    return render_template('index.html')
@app.route('/identification')
def identification():
    return render_template('identification.html')


if __name__ == '__main__':
    app.run(port=5005, debug=True)


