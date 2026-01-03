from flask import Flask, jsonify

app = Flask(__name__)

# Главная страница, чтобы проверить, что сервер жив
@app.route('/')
def home():
    return "To-Do List API is running!"

if __name__ == '__main__':
    app.run(debug=True)