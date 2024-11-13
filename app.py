from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for the battle page
@app.route('/battle')
def battle():
    return render_template('battle.html')

if __name__ == '__main__':
    app.run(debug=True)
