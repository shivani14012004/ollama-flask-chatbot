from flask import Flask, render_template, request
from llama import get_response

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form['message']

    bot_response = get_response(user_message)

    return render_template(
        'index.html',
        user_message=user_message,
        bot_response=bot_response
    )


if __name__ == '__main__':
    app.run(debug=True)