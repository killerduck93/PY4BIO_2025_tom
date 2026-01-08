from flask import Flask
app = Flask(__name__)

@app.route('/python/')
def index():
    return '<h1>Hello, Python!</h1>'

if __name__ == '__main__':
    app.run(debug=True)
    print(app.current_app())

