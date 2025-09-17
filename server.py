from flask import Flask, request

app = Flask(__name__)

@app.route('/exchange_token')
def exchange_token():
    code = request.args.get('code')
    return f"Your code is: {code}"

if __name__ == "__main__":
    app.run(port=5000)
