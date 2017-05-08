from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = "secret_key"


#main page 
@app.route('/')
def main():
    return render_template('main.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port = 8080, debug = True)
