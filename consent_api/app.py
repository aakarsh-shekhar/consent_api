from flask import Flask, request, redirect, jsonify

app = Flask(__name__)

@app.route("/")
def home_view():
        return "<h1>Hello World!</h1>"

# Start your app
if __name__ == '__main__':
    app.run(port=4242)
