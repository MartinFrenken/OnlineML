from flask import Flask, render_template

app = Flask(__name__)
@app.route('/')
def root():
    return render_template("app.html")
@app.route('/game')
def update():
    return render_template("app.html")
if __name__ == "__main__":
    app.run(debug=True)


